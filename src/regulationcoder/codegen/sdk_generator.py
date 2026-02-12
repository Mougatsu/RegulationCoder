"""SDKGenerator — uses Anthropic Claude to generate Python evaluation functions from rules."""

import json
import logging
import re

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.core.exceptions import CodeGenerationError
from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)

_CODEGEN_SYSTEM_PROMPT = """\
You are a senior Python engineer generating compliance evaluation functions from \
formalized regulatory rules.

CODE GENERATION RULES:
1. Generate a single Python function with the signature:
   def evaluate_{function_name}(profile: dict) -> str:
2. The function MUST return one of: "pass", "fail", or "not_applicable".
3. The function MUST include a docstring citing the source article.
4. Use safe dictionary access: profile.get("key") or nested_get helper.
5. Handle None values and missing keys gracefully — never raise KeyError or TypeError.
6. If a required input field is missing or None, return "not_applicable" (the system \
cannot be assessed without the data).
7. The function MUST be self-contained — no imports outside the standard library.
8. Include a nested helper function for resolving dotted field paths if needed.
9. Follow the evaluation logic from the rule specification exactly.
10. Add inline comments explaining the compliance logic.

OUTPUT FORMAT:
Return ONLY valid Python source code. Do NOT include markdown code fences. \
Do NOT include any explanatory text before or after the code. Return raw Python only."""


_CODEGEN_USER_TEMPLATE = """\
## Rule Specification

Rule ID: {rule_id}
Requirement ID: {requirement_id}
Rule Type: {rule_type}
Title: {title}
Description: {description}
Severity: {severity}
Article Reference: {article_ref}

### Inputs Needed (dotted field paths into the profile dict):
{inputs_list}

### Evaluation Logic (pseudocode):
{evaluation_logic}

### Remediation Guidance:
{remediation}

Generate a Python function `evaluate_{function_name}(profile: dict) -> str` that \
implements this rule's evaluation logic. The function must:
1. Resolve each input field from the profile dict using safe nested access.
2. Implement the evaluation logic faithfully.
3. Return "pass", "fail", or "not_applicable".
4. Include a docstring with the article reference and rule description.

Return ONLY the Python function code."""


class SDKGenerator:
    """Generate Python evaluation functions from compliance rules using Claude Sonnet.

    Usage:
        generator = SDKGenerator(settings)
        code = generator.generate(rule)
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.extraction_model

    def generate(self, rule: Rule) -> str:
        """Generate a Python evaluation function for a Rule.

        Args:
            rule: A Rule object to generate code for.

        Returns:
            A string containing valid Python source code with the evaluation function.

        Raises:
            CodeGenerationError: If the API call or code parsing fails.
        """
        function_name = self._rule_id_to_snake(rule.id)

        article_ref = ""
        if rule.citations:
            article_ref = rule.citations[0].article_ref
        if not article_ref:
            article_ref = f"Rule {rule.id}"

        inputs_list = "\n".join(f"- {inp}" for inp in rule.inputs_needed) or "- (none)"

        user_prompt = _CODEGEN_USER_TEMPLATE.format(
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            rule_type=rule.rule_type.value,
            title=rule.title,
            description=rule.description,
            severity=rule.severity.value,
            article_ref=article_ref,
            inputs_list=inputs_list,
            evaluation_logic=rule.evaluation_logic,
            remediation=rule.remediation,
            function_name=function_name,
        )

        logger.info("Generating SDK code for rule %s", rule.id)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=_CODEGEN_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except anthropic.APIError as e:
            raise CodeGenerationError(
                f"Anthropic API error during code generation for {rule.id}: {e}"
            ) from e

        raw_text = response.content[0].text
        code = self._extract_python_code(raw_text, rule.id)

        # Validate that the code defines the expected function
        expected_def = f"def evaluate_{function_name}"
        if expected_def not in code:
            logger.warning(
                "Generated code for %s does not contain expected function '%s'. "
                "Wrapping in expected signature.",
                rule.id,
                expected_def,
            )
            code = self._wrap_code(code, rule, function_name, article_ref)

        logger.info("Generated %d characters of Python code for rule %s", len(code), rule.id)
        return code

    def _extract_python_code(self, text: str, rule_id: str) -> str:
        """Extract Python code from Claude's response, stripping any markdown fences."""
        cleaned = text.strip()

        # Strip markdown code fences if present
        if "```python" in cleaned:
            parts = cleaned.split("```python", 1)
            if len(parts) > 1:
                cleaned = parts[1].split("```", 1)[0]
        elif "```" in cleaned:
            parts = cleaned.split("```", 1)
            if len(parts) > 1:
                cleaned = parts[1].split("```", 1)[0]

        cleaned = cleaned.strip()

        if not cleaned:
            raise CodeGenerationError(
                f"Empty code generated for rule {rule_id}"
            )

        return cleaned

    @staticmethod
    def _rule_id_to_snake(rule_id: str) -> str:
        """Convert a rule ID like 'RULE-EU-AI-ACT-010-02F-001' to a snake_case function suffix.

        Result: 'eu_ai_act_010_02f_001'
        """
        # Remove the RULE- prefix
        suffix = rule_id
        if suffix.upper().startswith("RULE-"):
            suffix = suffix[5:]
        # Replace hyphens with underscores and lowercase
        return suffix.replace("-", "_").lower()

    @staticmethod
    def _wrap_code(
        code: str, rule: Rule, function_name: str, article_ref: str
    ) -> str:
        """Wrap generated code in the expected function signature as a fallback."""
        indent = "    "
        docstring_lines = [
            f'{indent}"""Evaluate compliance for {rule.title}.',
            f"{indent}",
            f"{indent}Source: {article_ref}",
            f"{indent}Rule: {rule.id}",
            f"{indent}Severity: {rule.severity.value}",
            f"{indent}",
            f"{indent}Returns: 'pass', 'fail', or 'not_applicable'",
            f'{indent}"""',
        ]
        docstring = "\n".join(docstring_lines)

        # Indent the original code
        indented_body = "\n".join(f"{indent}{line}" for line in code.splitlines())

        return (
            f"def evaluate_{function_name}(profile: dict) -> str:\n"
            f"{docstring}\n"
            f"{indented_body}\n"
        )
