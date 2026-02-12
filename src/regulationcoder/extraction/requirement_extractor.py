"""RequirementExtractor — uses Anthropic Claude to extract structured requirements from clauses."""

import json
import logging
import re

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.core.exceptions import ExtractionError
from regulationcoder.extraction.prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_TEMPLATE,
)
from regulationcoder.models.citation import Citation
from regulationcoder.models.clause import Clause
from regulationcoder.models.requirement import Condition, Modality, Requirement

logger = logging.getLogger(__name__)


class RequirementExtractor:
    """Extract structured requirements from regulation clauses using Claude Sonnet.

    Usage:
        extractor = RequirementExtractor(settings)
        requirements = extractor.extract(clause)
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.extraction_model

    def extract(self, clause: Clause) -> list[Requirement]:
        """Extract all requirements from a single clause.

        Args:
            clause: A Clause object containing the regulation text to analyze.

        Returns:
            A list of Requirement objects extracted from the clause.

        Raises:
            ExtractionError: If the API call or parsing fails after retries.
        """
        article_ref = f"Article {clause.article_number}"
        if clause.paragraph_number is not None:
            article_ref += f"({clause.paragraph_number})"
        if clause.subsection_letter:
            article_ref += f"({clause.subsection_letter})"

        user_prompt = EXTRACTION_USER_TEMPLATE.format(
            clause_id=clause.id,
            article_ref=article_ref,
            clause_text=clause.text,
        )

        logger.info("Extracting requirements from clause %s", clause.id)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=EXTRACTION_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except anthropic.APIError as e:
            raise ExtractionError(
                f"Anthropic API error during extraction of clause {clause.id}: {e}"
            ) from e

        raw_text = response.content[0].text
        raw_items = self._parse_response(raw_text, clause.id)
        requirements = self._build_requirements(raw_items, clause)

        logger.info(
            "Extracted %d requirements from clause %s",
            len(requirements),
            clause.id,
        )
        return requirements

    def _parse_response(self, text: str, clause_id: str) -> list[dict]:
        """Parse the JSON array from Claude's response text.

        Handles responses that may be wrapped in markdown code fences.
        """
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
            # Attempt to extract JSON array from the response
            match = re.search(r"\[.*\]", cleaned, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group())
                except json.JSONDecodeError:
                    raise ExtractionError(
                        f"Failed to parse extraction response for clause {clause_id}: {e}"
                    ) from e
            else:
                raise ExtractionError(
                    f"No JSON array found in extraction response for clause {clause_id}: {e}"
                ) from e

        if not isinstance(parsed, list):
            raise ExtractionError(
                f"Expected JSON array from extraction, got {type(parsed).__name__} "
                f"for clause {clause_id}"
            )

        return parsed

    def _build_requirements(
        self, raw_items: list[dict], clause: Clause
    ) -> list[Requirement]:
        """Convert raw JSON dicts into validated Requirement objects."""
        requirements: list[Requirement] = []

        for seq, item in enumerate(raw_items, start=1):
            try:
                req = self._build_single_requirement(item, clause, seq)
                requirements.append(req)
            except (KeyError, ValueError) as e:
                logger.warning(
                    "Skipping malformed requirement %d from clause %s: %s",
                    seq,
                    clause.id,
                    e,
                )
                continue

        return requirements

    def _build_single_requirement(
        self, item: dict, clause: Clause, seq: int
    ) -> Requirement:
        """Build a single Requirement from a raw JSON dict."""
        # Build the requirement ID
        req_id = self._generate_requirement_id(clause, seq)

        # Parse modality
        modality_str = item.get("modality", "must").lower().strip()
        modality = self._parse_modality(modality_str)

        # Parse conditions
        conditions = [
            Condition(
                description=c.get("description", ""),
                clause_reference=c.get("clause_reference"),
            )
            for c in item.get("conditions", [])
            if isinstance(c, dict)
        ]

        # Parse exceptions
        exceptions = [
            Condition(
                description=e.get("description", ""),
                clause_reference=e.get("clause_reference"),
            )
            for e in item.get("exceptions", [])
            if isinstance(e, dict)
        ]

        # Build citation from the clause
        article_ref = f"Article {clause.article_number}"
        exact_quote = item.get("exact_quote", clause.text[:200])

        citation = Citation(
            clause_id=clause.id,
            article_ref=article_ref,
            paragraph_ref=(
                str(clause.paragraph_number) if clause.paragraph_number else None
            ),
            subsection_ref=clause.subsection_letter,
            page_number=clause.page_ref,
            exact_quote=exact_quote,
        )

        return Requirement(
            id=req_id,
            clause_id=clause.id,
            modality=modality,
            subject=item.get("subject", ""),
            action=item.get("action", ""),
            object=item.get("object", ""),
            conditions=conditions,
            exceptions=exceptions,
            scope=item.get("scope", ""),
            jurisdiction="European Union",
            confidence=float(item.get("confidence", 0.5)),
            ambiguity_notes=item.get("ambiguity_notes", ""),
            citations=[citation],
        )

    @staticmethod
    def _generate_requirement_id(clause: Clause, seq: int) -> str:
        """Generate a deterministic requirement ID.

        Format: REQ-EU-AI-ACT-{art:03d}-{para:02d}{sub}-{seq:03d}
        Example: REQ-EU-AI-ACT-010-02F-001
        """
        art_part = f"{clause.article_number:03d}"

        para_part = f"{clause.paragraph_number:02d}" if clause.paragraph_number else "00"

        sub_part = clause.subsection_letter.upper() if clause.subsection_letter else ""

        seq_part = f"{seq:03d}"

        return f"REQ-EU-AI-ACT-{art_part}-{para_part}{sub_part}-{seq_part}"

    @staticmethod
    def _parse_modality(modality_str: str) -> Modality:
        """Parse a modality string into a Modality enum value."""
        mapping = {
            "must": Modality.MUST,
            "must_not": Modality.MUST_NOT,
            "should": Modality.SHOULD,
            "should_not": Modality.SHOULD_NOT,
            "may": Modality.MAY,
            # Handle common alternatives
            "shall": Modality.MUST,
            "shall_not": Modality.MUST_NOT,
            "required": Modality.MUST,
            "prohibited": Modality.MUST_NOT,
            "recommended": Modality.SHOULD,
            "permitted": Modality.MAY,
        }
        return mapping.get(modality_str, Modality.MUST)
