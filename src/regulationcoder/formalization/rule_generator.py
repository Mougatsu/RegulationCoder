"""RuleGenerator — uses Anthropic Claude to formalize requirements into machine-checkable rules."""

import json
import logging
import re

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.core.exceptions import FormalizationError
from regulationcoder.formalization.prompts import (
    FORMALIZATION_SYSTEM_PROMPT,
    FORMALIZATION_USER_TEMPLATE,
)
from regulationcoder.models.citation import Citation
from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule, RuleType, Severity, TestCase

logger = logging.getLogger(__name__)


class RuleGenerator:
    """Generate machine-checkable compliance rules from requirements using Claude Sonnet.

    Usage:
        generator = RuleGenerator(settings)
        rule = generator.generate(requirement)
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.extraction_model

    def generate(self, requirement: Requirement) -> Rule:
        """Formalize a requirement into a machine-checkable Rule.

        Args:
            requirement: A Requirement object to formalize.

        Returns:
            A Rule object with evaluation logic, test cases, and metadata.

        Raises:
            FormalizationError: If the API call or parsing fails.
        """
        source_quote = ""
        if requirement.citations:
            source_quote = requirement.citations[0].exact_quote
        if not source_quote:
            source_quote = f"{requirement.subject} {requirement.action} {requirement.object}"

        conditions_str = "; ".join(c.description for c in requirement.conditions) or "None"
        exceptions_str = "; ".join(e.description for e in requirement.exceptions) or "None"

        user_prompt = FORMALIZATION_USER_TEMPLATE.format(
            requirement_id=requirement.id,
            clause_id=requirement.clause_id,
            modality=requirement.modality.value,
            subject=requirement.subject,
            action=requirement.action,
            object=requirement.object,
            scope=requirement.scope,
            conditions=conditions_str,
            exceptions=exceptions_str,
            confidence=requirement.confidence,
            source_quote=source_quote,
        )

        logger.info("Generating rule for requirement %s", requirement.id)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=FORMALIZATION_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except anthropic.APIError as e:
            raise FormalizationError(
                f"Anthropic API error during formalization of {requirement.id}: {e}"
            ) from e

        raw_text = response.content[0].text
        raw_rule = self._parse_response(raw_text, requirement.id)
        rule = self._build_rule(raw_rule, requirement)

        logger.info("Generated rule %s (type=%s)", rule.id, rule.rule_type.value)
        return rule

    def _parse_response(self, text: str, requirement_id: str) -> dict:
        """Parse the JSON object from Claude's response text."""
        cleaned = text.strip()

        # Strip markdown code fences if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):]
        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            # Attempt to extract a JSON object from the response
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group())
                except json.JSONDecodeError:
                    raise FormalizationError(
                        f"Failed to parse formalization response for {requirement_id}: {e}"
                    ) from e
            else:
                raise FormalizationError(
                    f"No JSON object found in formalization response for {requirement_id}: {e}"
                ) from e

        if not isinstance(parsed, dict):
            raise FormalizationError(
                f"Expected JSON object from formalization, got {type(parsed).__name__} "
                f"for {requirement_id}"
            )

        return parsed

    def _build_rule(self, raw: dict, requirement: Requirement) -> Rule:
        """Build a Rule object from raw JSON and the source requirement."""
        # Derive rule ID from requirement ID: REQ-... -> RULE-...
        rule_id = requirement.id.replace("REQ-", "RULE-", 1)

        # Parse rule type
        rule_type_str = raw.get("rule_type", "semi_automated").lower().strip()
        rule_type = self._parse_rule_type(rule_type_str)

        # Parse severity
        severity_str = raw.get("severity", "medium").lower().strip()
        severity = self._parse_severity(severity_str)

        # Parse test cases
        test_cases = self._parse_test_cases(raw.get("test_cases", []), rule_id)

        # Carry forward citations from the requirement
        citations: list[Citation] = list(requirement.citations)

        return Rule(
            id=rule_id,
            requirement_id=requirement.id,
            rule_type=rule_type,
            title=raw.get("title", f"Compliance check for {requirement.id}"),
            description=raw.get("description", ""),
            inputs_needed=raw.get("inputs_needed", []),
            evaluation_logic=raw.get("evaluation_logic", "result = 'manual_review'"),
            severity=severity,
            remediation=raw.get("remediation", ""),
            test_cases=test_cases,
            citations=citations,
        )

    @staticmethod
    def _parse_test_cases(raw_cases: list, rule_id: str) -> list[TestCase]:
        """Parse test case dicts into TestCase objects."""
        test_cases: list[TestCase] = []
        for idx, tc in enumerate(raw_cases, start=1):
            if not isinstance(tc, dict):
                continue
            test_id = f"TC-{rule_id.replace('RULE-', '')}-{idx:03d}"
            expected = tc.get("expected_result", "fail").lower().strip()
            if expected not in ("pass", "fail", "not_applicable"):
                expected = "fail"
            test_cases.append(
                TestCase(
                    id=test_id,
                    description=tc.get("description", f"Test case {idx}"),
                    input_data=tc.get("input_data", {}),
                    expected_result=expected,
                )
            )
        return test_cases

    @staticmethod
    def _parse_rule_type(rule_type_str: str) -> RuleType:
        """Parse a rule type string into a RuleType enum."""
        mapping = {
            "automated": RuleType.AUTOMATED,
            "semi_automated": RuleType.SEMI_AUTOMATED,
            "semi-automated": RuleType.SEMI_AUTOMATED,
            "manual": RuleType.MANUAL,
        }
        return mapping.get(rule_type_str, RuleType.SEMI_AUTOMATED)

    @staticmethod
    def _parse_severity(severity_str: str) -> Severity:
        """Parse a severity string into a Severity enum."""
        mapping = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
        }
        return mapping.get(severity_str, Severity.MEDIUM)
