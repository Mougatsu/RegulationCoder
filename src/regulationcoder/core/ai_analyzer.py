"""AI Compliance Analyzer — deep contextual analysis powered by Claude Opus 4.6.

Takes a SystemProfile and a deterministic ComplianceReport and sends them to
Claude Opus 4.6 for holistic, context-aware compliance analysis that goes
beyond what rule-based evaluation can capture.
"""

import json
import logging
from datetime import datetime, timezone

import httpx
import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.models.ai_analysis import AIAnalysisResult, AIInsight
from regulationcoder.models.evaluation import ComplianceReport
from regulationcoder.models.profile import SystemProfile

logger = logging.getLogger(__name__)

# ── System Prompt ───────────────────────────────────────────────────────

ANALYZER_SYSTEM_PROMPT = """\
You are a senior EU AI Act compliance analyst powered by Claude Opus 4.6,
working within the RegulationCoder platform. Your role is to provide deep,
contextual compliance analysis that complements the deterministic rule engine.

## Your Expertise

You have expert-level knowledge of:
- The EU Artificial Intelligence Act (Regulation (EU) 2024/1689) in its entirety
- The risk classification framework (unacceptable, high-risk, limited-risk, minimal-risk)
- Annex III high-risk categories and their specific requirements
- Articles 6-15 obligations for high-risk AI systems
- The interplay between the AI Act and GDPR, the EU Charter of Fundamental Rights,
  sector-specific regulations (e.g., MDR for medical devices, MiFID II for finance)
- Enforcement mechanisms, penalties (up to 35M EUR or 7% global turnover), and
  the phased compliance timeline

## Your Analysis Approach

1. **Holistic Assessment**: Look at the system profile as a whole. A system may tick
   individual boxes yet still present systemic compliance risks. For example, a
   recruitment AI that logs decisions but has no bias testing against protected groups
   has a fundamental gap that individual rule checks might not flag.

2. **Contextual Risk Identification**: Consider the DOMAIN and INTENDED PURPOSE when
   assessing risk. A facial recognition system used for law enforcement has very
   different risk implications than one used for phone unlocking. Identify risks that
   deterministic rules might miss, such as:
   - Automation bias risks specific to the deployment context
   - Data governance gaps given the sensitivity of the domain
   - Transparency shortfalls relative to the sophistication of the end users
   - Human oversight adequacy given the consequences of errors

3. **Actionable Remediation**: Provide SPECIFIC, PRACTICAL recommendations tailored
   to the system's domain and current maturity level. Instead of "improve documentation",
   say "create a model card documenting accuracy metrics disaggregated by the demographic
   groups identified in Annex III, Section 4(a) for employment systems."

4. **Regulatory Landscape**: Consider how the AI Act interacts with other applicable
   regulations. A health AI system must consider both the AI Act and the MDR. A system
   processing personal data must consider GDPR implications of Article 10 data governance.

5. **Honest Limitations**: Be transparent about areas where:
   - Automated analysis cannot substitute for human legal judgment
   - The profile data is insufficient to make a definitive assessment
   - Domain-specific expertise (medical, financial, etc.) is needed
   - Physical testing or audit would be required to verify claims

## Response Format

You MUST respond with ONLY valid JSON matching the following schema. Do NOT include
any text before or after the JSON. Do NOT wrap it in markdown code fences.

{
  "executive_summary": "2-4 sentence summary of the compliance posture",
  "overall_risk_level": "critical|high|medium|low",
  "risk_narrative": "Detailed narrative explaining the overall risk posture, key concerns, and how they relate to the specific system context",
  "key_strengths": ["strength 1", "strength 2", ...],
  "insights": [
    {
      "category": "risk_assessment|data_governance|transparency|human_oversight|accuracy|robustness|technical_documentation|record_keeping|general_compliance",
      "title": "Short descriptive title",
      "analysis": "Detailed analysis of this area, considering the system's specific context",
      "severity": "critical|high|medium|low|info",
      "recommendations": ["Specific actionable recommendation 1", ...],
      "relevant_articles": ["Article 9", "Article 10(2)(f)", ...]
    }
  ],
  "prioritized_actions": [
    "Highest priority action first",
    "Second priority action",
    ...
  ],
  "regulatory_context": "Broader regulatory context: how the AI Act interacts with other regulations applicable to this system, upcoming enforcement milestones, and strategic compliance considerations"
}

Provide 4-6 insights covering different categories. Prioritize the most
critical findings. Each insight must reference specific EU AI Act articles.

IMPORTANT: Keep your response CONCISE. Each analysis/narrative field should be
2-3 sentences max. Each recommendation should be one sentence. The total JSON
must fit within 6000 tokens. Brevity is essential.
"""

# ── User Prompt Template ────────────────────────────────────────────────

ANALYZER_USER_PROMPT = """\
## System Profile

The following is the complete profile of the AI system under evaluation:

```json
{profile_json}
```

## Deterministic Compliance Report Summary

The rule-based engine has already evaluated this system. Here are the results:

- **Report ID**: {report_id}
- **Regulation**: {regulation_id}
- **Overall Verdict**: {overall_verdict}
- **Compliance Score**: {compliance_score:.1f}%
- **Total Rules Evaluated**: {total_rules}
- **Passed**: {passed} | **Failed**: {failed} | **Not Applicable**: {not_applicable} | **Manual Review**: {manual_review}

### Critical Gaps ({critical_count})
{critical_gaps_text}

### High Gaps ({high_count})
{high_gaps_text}

### Medium Gaps ({medium_count})
{medium_gaps_text}

### Failed Rule Details
{failed_rules_text}

## Your Task

Perform a deep, contextual compliance analysis of this AI system. Go beyond the
deterministic rule results:

1. Assess the OVERALL compliance posture holistically
2. Identify risks the rule engine may have missed given the system's specific
   purpose and domain
3. Evaluate the adequacy of measures relative to the system's risk level
4. Provide prioritized, actionable remediation guidance
5. Consider the broader regulatory context

Remember: respond with ONLY valid JSON matching the schema described in your instructions.
"""


def _format_gaps(gaps: list) -> str:
    """Format compliance gaps into readable text for the prompt."""
    if not gaps:
        return "  None identified."
    lines = []
    for gap in gaps:
        lines.append(
            f"  - **[{gap.severity.upper()}]** {gap.description}\n"
            f"    Rule: {gap.rule_id} | Article: {gap.article_ref}\n"
            f"    Remediation: {gap.remediation}"
        )
    return "\n".join(lines)


def _format_failed_rules(rule_results: list) -> str:
    """Format failed rule results into readable text for the prompt."""
    failed = [r for r in rule_results if r.verdict.value == "fail"]
    if not failed:
        return "  No failed rules."
    lines = []
    for r in failed:
        lines.append(
            f"  - **{r.title}** ({r.rule_id})\n"
            f"    Severity: {r.severity} | Article: {r.article_ref}\n"
            f"    Details: {r.details}\n"
            f"    Remediation: {r.remediation}"
        )
    return "\n".join(lines)


class ComplianceAnalyzer:
    """AI-powered compliance analyzer using Claude Opus 4.6.

    Complements the deterministic rule engine by providing holistic,
    context-aware analysis of a system's EU AI Act compliance posture.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key,
            timeout=httpx.Timeout(300.0, connect=30.0),
        )
        self.model = settings.judge_model

    def _build_user_prompt(
        self, profile: SystemProfile, report: ComplianceReport
    ) -> str:
        """Build the user prompt from the profile and compliance report."""
        profile_json = profile.model_dump_json(indent=2)

        return ANALYZER_USER_PROMPT.format(
            profile_json=profile_json,
            report_id=report.id,
            regulation_id=report.regulation_id,
            overall_verdict=report.overall_verdict,
            compliance_score=report.summary.compliance_score,
            total_rules=report.summary.total_rules,
            passed=report.summary.passed,
            failed=report.summary.failed,
            not_applicable=report.summary.not_applicable,
            manual_review=report.summary.manual_review,
            critical_count=len(report.critical_gaps),
            critical_gaps_text=_format_gaps(report.critical_gaps),
            high_count=len(report.high_gaps),
            high_gaps_text=_format_gaps(report.high_gaps),
            medium_count=len(report.medium_gaps),
            medium_gaps_text=_format_gaps(report.medium_gaps),
            failed_rules_text=_format_failed_rules(report.rule_results),
        )

    @staticmethod
    def _repair_truncated_json(text: str) -> str:
        """Attempt to repair JSON that was truncated due to max_tokens.

        Closes any open strings, arrays, and objects so json.loads can parse it.
        """
        # Strip markdown fences first
        cleaned = text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1]
            if "```" in cleaned:
                cleaned = cleaned.split("```")[0]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
            if "```" in cleaned:
                cleaned = cleaned.split("```")[0]
        cleaned = cleaned.strip()

        # Try to find the last successfully parseable position
        # by progressively adding closing characters
        in_string = False
        escape_next = False
        depth_obj = 0
        depth_arr = 0
        last_good = 0

        for i, ch in enumerate(cleaned):
            if escape_next:
                escape_next = False
                continue
            if ch == "\\":
                escape_next = True
                continue
            if ch == '"' and not escape_next:
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == "{":
                depth_obj += 1
            elif ch == "}":
                depth_obj -= 1
            elif ch == "[":
                depth_arr += 1
            elif ch == "]":
                depth_arr -= 1
            if depth_obj >= 0 and depth_arr >= 0:
                last_good = i

        # Build repair suffix
        repaired = cleaned[: last_good + 1]
        if in_string:
            repaired += '"'
        repaired += "]" * max(0, depth_arr)
        repaired += "}" * max(0, depth_obj)

        return repaired

    def _parse_response(self, text: str) -> dict:
        """Parse JSON from the model response, stripping markdown fences if present."""
        cleaned = text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0]
        return json.loads(cleaned.strip())

    def analyze(
        self, profile: SystemProfile, report: ComplianceReport
    ) -> AIAnalysisResult:
        """Perform deep AI-powered compliance analysis.

        Args:
            profile: The AI system's profile with all declared properties.
            report: The deterministic compliance report from the rule engine.

        Returns:
            AIAnalysisResult with executive summary, insights, and recommendations.

        Raises:
            RuntimeError: If the API call fails after retries or the response
                cannot be parsed into a valid AIAnalysisResult.
        """
        now = datetime.now(timezone.utc)
        analysis_id = (
            f"AI-ANALYSIS-{report.id}-{now.strftime('%Y%m%dT%H%M%S')}"
        )

        user_prompt = self._build_user_prompt(profile, report)

        logger.info(
            "Starting AI analysis for system '%s' (report %s) using model %s",
            profile.system_name,
            report.id,
            self.model,
        )

        last_error: Exception | None = None
        max_attempts = self.settings.max_judge_retries + 1

        for attempt in range(1, max_attempts + 1):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=8192,
                    system=ANALYZER_SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                raw_text = response.content[0].text
                stop_reason = response.stop_reason
                logger.debug(
                    "AI analysis response received (%d chars, stop=%s, attempt %d/%d)",
                    len(raw_text),
                    stop_reason,
                    attempt,
                    max_attempts,
                )

                # If truncated, try to repair the JSON
                if stop_reason == "max_tokens":
                    raw_text = self._repair_truncated_json(raw_text)

                raw = self._parse_response(raw_text)

                # Build insights from the parsed response
                insights = []
                for item in raw.get("insights", []):
                    insights.append(
                        AIInsight(
                            category=item.get("category", "general_compliance"),
                            title=item.get("title", ""),
                            analysis=item.get("analysis", ""),
                            severity=item.get("severity", "medium"),
                            recommendations=item.get("recommendations", []),
                            relevant_articles=item.get("relevant_articles", []),
                        )
                    )

                result = AIAnalysisResult(
                    id=analysis_id,
                    report_id=report.id,
                    model_used=self.model,
                    executive_summary=raw.get("executive_summary", ""),
                    overall_risk_level=raw.get("overall_risk_level", "medium"),
                    risk_narrative=raw.get("risk_narrative", ""),
                    key_strengths=raw.get("key_strengths", []),
                    insights=insights,
                    prioritized_actions=raw.get("prioritized_actions", []),
                    regulatory_context=raw.get("regulatory_context", ""),
                    timestamp=now,
                )

                logger.info(
                    "AI analysis complete for '%s': risk_level=%s, insights=%d, actions=%d",
                    profile.system_name,
                    result.overall_risk_level,
                    len(result.insights),
                    len(result.prioritized_actions),
                )
                return result

            except json.JSONDecodeError as exc:
                last_error = exc
                logger.warning(
                    "Failed to parse AI analysis JSON (attempt %d/%d): %s",
                    attempt,
                    max_attempts,
                    exc,
                )
            except anthropic.APIError as exc:
                last_error = exc
                logger.warning(
                    "Anthropic API error during AI analysis (attempt %d/%d): %s",
                    attempt,
                    max_attempts,
                    exc,
                )
            except anthropic.APIConnectionError as exc:
                last_error = exc
                logger.warning(
                    "Anthropic API connection error (attempt %d/%d): %s",
                    attempt,
                    max_attempts,
                    exc,
                )

        raise RuntimeError(
            f"AI analysis failed after {max_attempts} attempts for report "
            f"{report.id}: {last_error}"
        ) from last_error
