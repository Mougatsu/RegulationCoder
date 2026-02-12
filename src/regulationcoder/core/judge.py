"""Anthropic Judge Gates — quality assurance at every pipeline stage.

Each gate uses Claude Opus as an auditor to verify outputs against source text,
ensuring no hallucinations, correct modality, and faithful implementation.
"""

import json
import logging
from datetime import datetime, timezone

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.models.judge_report import (
    Finding,
    FindingSeverity,
    FindingType,
    JudgeReport,
    JudgeScores,
    Verdict,
)

logger = logging.getLogger(__name__)

# ── Gate A: Requirements Validation ──────────────────────────────────

GATE_A_SYSTEM = """You are a senior legal-AI auditor verifying that extracted regulatory requirements
are FAITHFULLY grounded in the source legal text, without hallucination, omission,
or misinterpretation.

Score each dimension 0.0-1.0:
- GROUNDING: Does every field map to explicit text in the clause?
- HALLUCINATION RISK: Any fabricated obligations, subjects, or conditions? (lower=better)
  Modality mapping: "shall"->must, "should"->should, "may"->may, "shall not"->must_not
- AMBIGUITY: Does the requirement acknowledge genuine ambiguities?
- IMPLEMENTABILITY: Can this requirement be practically verified?

CRITICAL RULES:
- If ANY obligation is not present in the source text, flag as hallucination (critical).
- If the modality is wrong, flag as critical modality_error.
- If the subject is wrong, flag as critical subject_error.

Respond with ONLY valid JSON matching this schema:
{
  "verdict": "approve|revise|block",
  "scores": {
    "grounding_score": 0.0-1.0,
    "hallucination_risk": 0.0-1.0,
    "ambiguity_score": 0.0-1.0,
    "implementability_score": 0.0-1.0,
    "test_adequacy_score": 0.0-1.0,
    "overall_confidence": 0.0-1.0
  },
  "findings": [
    {
      "finding_type": "hallucination|modality_error|subject_error|omission|ambiguity",
      "severity": "critical|major|minor|info",
      "description": "...",
      "affected_field": "...",
      "suggested_fix": "..."
    }
  ],
  "citations_checked": ["clause_id_1", "clause_id_2"]
}"""

GATE_A_USER = """## Source Clause
Clause ID: {clause_id}
Article: {article_ref}
Text:
\"\"\"{clause_text}\"\"\"

## Parent Article Context
{parent_context}

## Extracted Requirement (to validate)
```json
{requirement_json}
```

Evaluate whether this requirement is faithfully grounded in the source clause.
Apply the blocking policy:
- BLOCK if hallucination_risk > 0.5 OR grounding_score < 0.5 OR critical finding
- REVISE if grounding_score < 0.8 OR ambiguity_score > 0.7 OR major finding
- APPROVE otherwise"""

# ── Gate B: Rule Formalization Validation ────────────────────────────

GATE_B_SYSTEM = """You are a senior compliance engineer verifying that formalized rules correctly
implement their source requirements. Verify evaluation logic is sound and test
cases are adequate.

Score each dimension 0.0-1.0:
- GROUNDING: Does the rule faithfully implement the requirement?
- HALLUCINATION RISK: Any fabricated evaluation conditions?
- IMPLEMENTABILITY: Can the evaluation logic be implemented in code?
- TEST ADEQUACY: Do test cases cover pass, fail, and not_applicable paths?

Respond with ONLY valid JSON matching the same schema as Gate A."""

GATE_B_USER = """## Source Requirement
```json
{requirement_json}
```

## Formalized Rule (to validate)
```json
{rule_json}
```

Evaluate whether this rule correctly implements the requirement.
Apply the blocking policy:
- BLOCK if grounding_score < 0.5 OR critical logic_error
- REVISE if implementability_score < 0.7 OR test_adequacy_score < 0.6 OR major finding
- APPROVE otherwise"""

# ── Gate C: Code Generation Validation ───────────────────────────────

GATE_C_SYSTEM = """You are a senior software engineer reviewing auto-generated Python compliance code.

Verify that the code:
1. CORRECTLY implements the rule's evaluation logic
2. HANDLES edge cases (None inputs, missing fields, type mismatches)
3. PRODUCES correct verdicts matching the rule specification
4. Has ADEQUATE test coverage
5. Correctly CITES source articles in docstrings

CRITICAL: If the code produces a WRONG verdict for any realistic input, this is a
critical finding that BLOCKS approval.

Respond with ONLY valid JSON matching the same schema as other gates."""

GATE_C_USER = """## Source Rule
```json
{rule_json}
```

## Generated Python Code
```python
{generated_code}
```

## Generated Test Code
```python
{test_code}
```

Mentally trace execution for each test case. Verify correctness.
Apply the blocking policy:
- BLOCK if grounding_score < 0.6 OR critical finding OR syntax errors
- REVISE if test_adequacy_score < 0.7 OR major findings
- APPROVE otherwise"""

# ── Gate D: Diff Impact Validation ───────────────────────────────────

GATE_D_SYSTEM = """You are a senior regulatory change analyst verifying that a diff impact analysis
is correct and complete.

Verify that:
1. All changed clauses are identified
2. Semantic classification (substantive/editorial/structural/clarification) is correct
3. All impacted requirements and rules are traced
4. No critical impacts are missed

Respond with ONLY valid JSON matching the same schema as other gates."""

GATE_D_USER = """## Regulation Diff
Old version: {old_version}
New version: {new_version}

## Clause Changes
```json
{changes_json}
```

## Impact Analysis (to validate)
```json
{impact_json}
```

Apply the blocking policy:
- BLOCK if grounding_score < 0.5 OR missed impact on critical rule
- REVISE if any major finding
- APPROVE otherwise"""


class JudgeGate:
    """Base class for Anthropic judge gates."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.judge_model

    def _call_judge(self, system_prompt: str, user_prompt: str) -> dict:
        """Call the Anthropic judge model and parse the JSON response."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())

    def _build_report(
        self, stage: str, target_ids: list[str], raw: dict
    ) -> JudgeReport:
        """Build a JudgeReport from raw judge output."""
        scores_raw = raw.get("scores", {})
        scores = JudgeScores(
            grounding_score=scores_raw.get("grounding_score", 0.0),
            hallucination_risk=scores_raw.get("hallucination_risk", 0.0),
            ambiguity_score=scores_raw.get("ambiguity_score", 0.0),
            implementability_score=scores_raw.get("implementability_score", 0.0),
            test_adequacy_score=scores_raw.get("test_adequacy_score", 0.0),
            overall_confidence=scores_raw.get("overall_confidence", 0.0),
        )
        findings = []
        for f in raw.get("findings", []):
            try:
                findings.append(
                    Finding(
                        finding_type=FindingType(f.get("finding_type", "ambiguity")),
                        severity=FindingSeverity(f.get("severity", "info")),
                        description=f.get("description", ""),
                        affected_field=f.get("affected_field", ""),
                        suggested_fix=f.get("suggested_fix", ""),
                    )
                )
            except ValueError:
                findings.append(
                    Finding(
                        finding_type=FindingType.AMBIGUITY,
                        severity=FindingSeverity.INFO,
                        description=f.get("description", str(f)),
                    )
                )

        now = datetime.now(timezone.utc)
        report_id = f"JUDGE-{stage.upper()}-{'-'.join(target_ids)[:50]}-{now.strftime('%Y%m%d%H%M%S')}"

        return JudgeReport(
            id=report_id,
            stage=stage,
            target_ids=target_ids,
            verdict=Verdict(raw.get("verdict", "block")),
            scores=scores,
            findings=findings,
            citations_checked=raw.get("citations_checked", []),
            model_used=self.model,
            timestamp=now,
        )


class GateA(JudgeGate):
    """Gate A — Requirements Validation (after extraction)."""

    def evaluate(
        self,
        clause_id: str,
        clause_text: str,
        article_ref: str,
        parent_context: str,
        requirement_json: str,
    ) -> JudgeReport:
        """Validate an extracted requirement against its source clause."""
        user_prompt = GATE_A_USER.format(
            clause_id=clause_id,
            article_ref=article_ref,
            clause_text=clause_text,
            parent_context=parent_context,
            requirement_json=requirement_json,
        )
        logger.info("Gate A evaluating requirement for clause %s", clause_id)
        raw = self._call_judge(GATE_A_SYSTEM, user_prompt)
        return self._build_report("gate_a_extraction", [clause_id], raw)


class GateB(JudgeGate):
    """Gate B — Rule Formalization Validation (after formalization)."""

    def evaluate(
        self, requirement_json: str, rule_json: str
    ) -> JudgeReport:
        """Validate a formalized rule against its source requirement."""
        user_prompt = GATE_B_USER.format(
            requirement_json=requirement_json,
            rule_json=rule_json,
        )
        raw = self._call_judge(GATE_B_SYSTEM, user_prompt)
        rule_data = json.loads(rule_json)
        return self._build_report(
            "gate_b_formalization", [rule_data.get("id", "unknown")], raw
        )


class GateC(JudgeGate):
    """Gate C — Code Generation Validation (after code gen)."""

    def evaluate(
        self, rule_json: str, generated_code: str, test_code: str
    ) -> JudgeReport:
        """Validate generated code against its source rule."""
        user_prompt = GATE_C_USER.format(
            rule_json=rule_json,
            generated_code=generated_code,
            test_code=test_code,
        )
        raw = self._call_judge(GATE_C_SYSTEM, user_prompt)
        rule_data = json.loads(rule_json)
        return self._build_report(
            "gate_c_codegen", [rule_data.get("id", "unknown")], raw
        )


class GateD(JudgeGate):
    """Gate D — Diff Impact Analysis Validation."""

    def evaluate(
        self,
        old_version: str,
        new_version: str,
        changes_json: str,
        impact_json: str,
    ) -> JudgeReport:
        """Validate a diff impact analysis."""
        user_prompt = GATE_D_USER.format(
            old_version=old_version,
            new_version=new_version,
            changes_json=changes_json,
            impact_json=impact_json,
        )
        raw = self._call_judge(GATE_D_SYSTEM, user_prompt)
        return self._build_report(
            "gate_d_diff", [f"{old_version}->{new_version}"], raw
        )
