"""ManualControlGenerator — generates human verification procedures for non-automated rules."""

import json
import logging
import re

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.core.exceptions import FormalizationError
from regulationcoder.formalization.prompts import (
    MANUAL_CONTROL_SYSTEM_PROMPT,
    MANUAL_CONTROL_USER_TEMPLATE,
)
from regulationcoder.models.citation import Citation
from regulationcoder.models.manual_control import ManualControl
from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)

# Explanations for rule types used in prompts
_RULE_TYPE_EXPLANATIONS = {
    "manual": (
        "it requires entirely human assessment and cannot be checked automatically"
    ),
    "semi_automated": (
        "some aspects can be checked automatically but qualitative aspects "
        "require human review"
    ),
    "automated": (
        "it can be fully checked automatically, but a manual control is requested "
        "as an additional safeguard"
    ),
}


class ManualControlGenerator:
    """Generate manual verification controls for requirements with manual or semi-automated rules.

    Usage:
        generator = ManualControlGenerator(settings)
        control = generator.generate(requirement, rule)
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.extraction_model

    def generate(self, requirement: Requirement, rule: Rule) -> ManualControl:
        """Generate a ManualControl for a requirement/rule pair.

        This is primarily intended for rules of type "manual" or "semi_automated",
        but can be called for any rule when an additional human verification
        procedure is desired.

        Args:
            requirement: The source Requirement.
            rule: The associated Rule.

        Returns:
            A ManualControl with verification steps and evidence requirements.

        Raises:
            FormalizationError: If the API call or parsing fails.
        """
        source_quote = ""
        if requirement.citations:
            source_quote = requirement.citations[0].exact_quote
        if not source_quote:
            source_quote = f"{requirement.subject} {requirement.action} {requirement.object}"

        rule_type_str = rule.rule_type.value
        rule_type_explanation = _RULE_TYPE_EXPLANATIONS.get(
            rule_type_str,
            "its automation level requires supplemental human verification",
        )

        user_prompt = MANUAL_CONTROL_USER_TEMPLATE.format(
            requirement_id=requirement.id,
            modality=requirement.modality.value,
            subject=requirement.subject,
            action=requirement.action,
            object=requirement.object,
            scope=requirement.scope,
            rule_id=rule.id,
            rule_type=rule_type_str,
            rule_title=rule.title,
            rule_description=rule.description,
            source_quote=source_quote,
            rule_type_explanation=rule_type_explanation,
        )

        logger.info(
            "Generating manual control for requirement %s (rule %s)",
            requirement.id,
            rule.id,
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=MANUAL_CONTROL_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except anthropic.APIError as e:
            raise FormalizationError(
                f"Anthropic API error during manual control generation for "
                f"{requirement.id}: {e}"
            ) from e

        raw_text = response.content[0].text
        raw_control = self._parse_response(raw_text, requirement.id)
        control = self._build_control(raw_control, requirement, rule)

        logger.info("Generated manual control %s", control.id)
        return control

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
                        f"Failed to parse manual control response for "
                        f"{requirement_id}: {e}"
                    ) from e
            else:
                raise FormalizationError(
                    f"No JSON object found in manual control response for "
                    f"{requirement_id}: {e}"
                ) from e

        if not isinstance(parsed, dict):
            raise FormalizationError(
                f"Expected JSON object from manual control generation, "
                f"got {type(parsed).__name__} for {requirement_id}"
            )

        return parsed

    @staticmethod
    def _build_control(
        raw: dict, requirement: Requirement, rule: Rule
    ) -> ManualControl:
        """Build a ManualControl from raw JSON, requirement, and rule."""
        # Derive control ID: REQ-... -> CTRL-...
        control_id = requirement.id.replace("REQ-", "CTRL-", 1)

        # Carry forward citations
        citations: list[Citation] = list(requirement.citations)

        return ManualControl(
            id=control_id,
            rule_id=rule.id,
            requirement_id=requirement.id,
            title=raw.get("title", f"Manual verification for {requirement.id}"),
            description=raw.get("description", ""),
            verification_steps=raw.get("verification_steps", []),
            evidence_required=raw.get("evidence_required", []),
            citations=citations,
        )
