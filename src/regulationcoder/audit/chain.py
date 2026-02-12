"""AuditChainVerifier — verify the integrity of hash-chained audit logs."""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any

from regulationcoder.models.audit_entry import AuditAction, AuditEntry

logger = logging.getLogger(__name__)

_GENESIS_HASH = "0" * 64


class AuditChainVerifier:
    """Verify the hash chain of an audit JSONL log file.

    Each entry's ``entry_hash`` must equal:

        SHA-256(previous_hash | timestamp_iso | action | target_ids_json | details_json)

    and its ``previous_hash`` must match the ``entry_hash`` of the preceding entry
    (or the genesis hash ``"0" * 64`` for the first entry).
    """

    def verify(self, log_dir: str) -> tuple[bool, list[str]]:
        """Verify the full chain in the audit log.

        Parameters
        ----------
        log_dir:
            Directory containing the ``audit.jsonl`` file.

        Returns
        -------
        tuple[bool, list[str]]
            ``(is_valid, errors)`` where *is_valid* is ``True`` when every
            entry passes verification and *errors* is a list of human-readable
            error descriptions (empty when valid).
        """
        log_file = os.path.join(log_dir, "audit.jsonl")
        errors: list[str] = []

        if not os.path.exists(log_file):
            errors.append(f"Audit log file not found: {log_file}")
            return False, errors

        entries: list[dict[str, Any]] = []
        with open(log_file, "r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    entry = json.loads(stripped)
                    entries.append(entry)
                except json.JSONDecodeError as exc:
                    errors.append(f"Line {line_no}: invalid JSON — {exc}")

        if not entries and not errors:
            # Empty log is technically valid
            return True, []

        if errors:
            # JSON parse errors already found
            return False, errors

        expected_previous = _GENESIS_HASH

        for idx, entry in enumerate(entries):
            entry_id = entry.get("id", f"<index {idx}>")
            stored_previous = entry.get("previous_hash", "")
            stored_hash = entry.get("entry_hash", "")

            # 1. Check previous_hash linkage
            if stored_previous != expected_previous:
                errors.append(
                    f"Entry {entry_id} (index {idx}): previous_hash mismatch. "
                    f"Expected '{expected_previous[:16]}...', "
                    f"got '{stored_previous[:16]}...'."
                )

            # 2. Recompute hash and compare
            try:
                action_value = entry.get("action", "")
                timestamp_str = entry.get("timestamp", "")
                target_ids = entry.get("target_ids", [])
                details = entry.get("details", {})

                computed = self._compute_hash(
                    previous_hash=stored_previous,
                    timestamp_iso=timestamp_str,
                    action_value=action_value,
                    target_ids=target_ids,
                    details=details,
                )

                if computed != stored_hash:
                    errors.append(
                        f"Entry {entry_id} (index {idx}): entry_hash mismatch. "
                        f"Computed '{computed[:16]}...', "
                        f"stored '{stored_hash[:16]}...'."
                    )
            except Exception as exc:
                errors.append(
                    f"Entry {entry_id} (index {idx}): failed to recompute hash — {exc}"
                )

            # Advance the chain
            expected_previous = stored_hash

        is_valid = len(errors) == 0
        if is_valid:
            logger.info("Audit chain verified: %d entries, all valid.", len(entries))
        else:
            logger.warning(
                "Audit chain verification failed: %d entries, %d errors.",
                len(entries),
                len(errors),
            )
        return is_valid, errors

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_hash(
        previous_hash: str,
        timestamp_iso: str,
        action_value: str,
        target_ids: list[str],
        details: dict[str, Any],
    ) -> str:
        """Recompute the SHA-256 entry hash using the same formula as AuditLogger."""
        parts = [
            previous_hash,
            timestamp_iso,
            action_value,
            json.dumps(target_ids, sort_keys=True),
            json.dumps(details, sort_keys=True, default=str),
        ]
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
