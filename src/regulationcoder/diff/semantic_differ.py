"""SemanticDiffer — classify clause changes using Claude."""

import json
import logging

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.models.diff import ChangeType, ClauseChange, SemanticChangeType

logger = logging.getLogger(__name__)

_CLASSIFICATION_PROMPT = """\
You are a legal-text analyst. For each regulation clause change below,
classify it into exactly ONE of these semantic categories:

- **substantive**: Changes the legal obligation, right, prohibition, or scope.
- **editorial**: Fixes grammar, spelling, punctuation, or formatting only.
- **structural**: Re-numbers, moves, or splits/merges clauses without changing meaning.
- **clarification**: Adds detail or examples to an existing obligation without altering it.

Respond with a JSON array of objects, one per change, in the same order as the
input.  Each object must have:
  - "clause_id": the clause ID (string)
  - "semantic_type": one of "substantive", "editorial", "structural", "clarification"

Input changes (JSON):
{changes_json}

Respond ONLY with the JSON array — no markdown fences, no commentary.
"""


class SemanticDiffer:
    """Use Claude to semantically classify each ClauseChange.

    Only MODIFIED changes are sent to the model; ADDED changes default to
    ``substantive`` and DELETED changes default to ``substantive`` as well,
    since they inherently alter obligations.  UNCHANGED clauses are skipped.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.extraction_model

    def classify(self, changes: list[ClauseChange]) -> list[ClauseChange]:
        """Classify each ClauseChange and update its ``semantic_type`` field.

        Returns the same list (mutated in-place) for convenience.
        """
        # Separate changes that need LLM classification from those we can
        # assign deterministically.
        to_classify: list[ClauseChange] = []

        for change in changes:
            if change.change_type == ChangeType.UNCHANGED:
                # No semantic change — leave semantic_type as None
                continue
            elif change.change_type in (ChangeType.ADDED, ChangeType.DELETED):
                change.semantic_type = SemanticChangeType.SUBSTANTIVE
            elif change.change_type == ChangeType.MODIFIED:
                to_classify.append(change)

        if not to_classify:
            logger.info("SemanticDiffer: nothing to classify (no MODIFIED changes).")
            return changes

        # Build the prompt payload — only send clause_id, old_text, new_text
        payload = [
            {
                "clause_id": c.clause_id,
                "old_text": c.old_text[:2000],  # truncate for token economy
                "new_text": c.new_text[:2000],
            }
            for c in to_classify
        ]

        # Process in batches of 20 to stay within context limits
        batch_size = 20
        classification_map: dict[str, SemanticChangeType] = {}

        for i in range(0, len(payload), batch_size):
            batch = payload[i : i + batch_size]
            batch_map = self._classify_batch(batch)
            classification_map.update(batch_map)

        # Apply classifications back to the changes
        valid_types = {t.value for t in SemanticChangeType}
        for change in to_classify:
            classified = classification_map.get(change.clause_id)
            if classified:
                change.semantic_type = classified
            else:
                # Fallback if the model didn't return a classification
                change.semantic_type = SemanticChangeType.SUBSTANTIVE
                logger.warning(
                    "No classification returned for clause %s; defaulting to substantive.",
                    change.clause_id,
                )

        logger.info(
            "SemanticDiffer: classified %d MODIFIED changes via LLM.", len(to_classify)
        )
        return changes

    def _classify_batch(
        self, batch: list[dict]
    ) -> dict[str, SemanticChangeType]:
        """Send a batch of changes to Claude for classification."""
        prompt = _CLASSIFICATION_PROMPT.format(changes_json=json.dumps(batch, indent=2))

        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()

            # Parse the JSON response — strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1]
                if raw.endswith("```"):
                    raw = raw[: raw.rfind("```")]

            classifications = json.loads(raw)
        except (json.JSONDecodeError, anthropic.APIError, IndexError, KeyError) as exc:
            logger.error("SemanticDiffer LLM classification failed: %s", exc)
            # Fall back to substantive for all items in this batch
            return {
                item["clause_id"]: SemanticChangeType.SUBSTANTIVE for item in batch
            }

        valid_types = {t.value: t for t in SemanticChangeType}
        result: dict[str, SemanticChangeType] = {}

        for item in classifications:
            cid = item.get("clause_id", "")
            stype_str = item.get("semantic_type", "")
            if stype_str in valid_types:
                result[cid] = valid_types[stype_str]
            else:
                result[cid] = SemanticChangeType.SUBSTANTIVE

        return result
