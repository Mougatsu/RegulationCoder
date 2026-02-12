"""AuditLogger — append-only, hash-chained audit trail in JSONL format."""

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any

from regulationcoder.models.audit_entry import AuditAction, AuditEntry

logger = logging.getLogger(__name__)

# Sentinel for the very first entry in a fresh log
_GENESIS_HASH = "0" * 64


class AuditLogger:
    """Append-only audit logger that writes hash-chained JSONL entries.

    Each entry's ``entry_hash`` is computed as:

        SHA-256(previous_hash + timestamp_iso + action + target_ids_json + details_json)

    This guarantees tamper evidence: modifying or removing any entry breaks
    the chain and can be detected by :class:`AuditChainVerifier`.
    """

    def __init__(self, log_dir: str) -> None:
        self.log_dir = log_dir
        self._log_file = os.path.join(log_dir, "audit.jsonl")
        os.makedirs(log_dir, exist_ok=True)
        self._previous_hash = self._read_last_hash()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def log(
        self,
        action: AuditAction,
        stage: str,
        target_ids: list[str] | None = None,
        details: dict[str, Any] | None = None,
        actor: str = "system",
        input_hash: str = "",
        output_hash: str = "",
        model_used: str = "",
        verdict: str = "",
    ) -> AuditEntry:
        """Create, persist, and return a new audit entry.

        Parameters
        ----------
        action:
            The auditable action type.
        stage:
            Pipeline stage name (e.g. ``"ingestion"``, ``"codegen"``).
        target_ids:
            IDs of artefacts affected by this action.
        details:
            Arbitrary metadata dict.
        actor:
            Who/what performed the action (default ``"system"``).
        input_hash:
            Optional SHA-256 of the input data.
        output_hash:
            Optional SHA-256 of the output data.
        model_used:
            LLM model identifier used, if any.
        verdict:
            Evaluation verdict, if applicable.
        """
        target_ids = target_ids or []
        details = details or {}
        now = datetime.now(timezone.utc)

        entry_hash = self._compute_hash(
            previous_hash=self._previous_hash,
            timestamp_iso=self._normalize_timestamp(now),
            action=action,
            target_ids=target_ids,
            details=details,
        )

        entry = AuditEntry(
            id=str(uuid.uuid4()),
            timestamp=now,
            action=action,
            stage=stage,
            actor=actor,
            target_ids=target_ids,
            input_hash=input_hash,
            output_hash=output_hash,
            previous_hash=self._previous_hash,
            entry_hash=entry_hash,
            details=details,
            model_used=model_used,
            verdict=verdict,
        )

        self._append(entry)
        self._previous_hash = entry_hash

        logger.debug(
            "Audit entry %s: action=%s stage=%s targets=%s",
            entry.id,
            action.value,
            stage,
            target_ids,
        )
        return entry

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_timestamp(dt: datetime) -> str:
        """Produce the same ISO-8601 string that Pydantic v2 writes to JSON.

        Pydantic serializes ``datetime(…, tzinfo=timezone.utc)`` as
        ``"2024-01-01T00:00:00Z"`` (with *Z* instead of *+00:00*).  We must
        use the identical representation when computing the hash so the
        verifier — which reads back the Pydantic-serialized timestamp — can
        reproduce it.
        """
        iso = dt.isoformat()
        if iso.endswith("+00:00"):
            iso = iso[:-6] + "Z"
        return iso

    @staticmethod
    def _compute_hash(
        previous_hash: str,
        timestamp_iso: str,
        action: AuditAction,
        target_ids: list[str],
        details: dict[str, Any],
    ) -> str:
        """Compute the SHA-256 entry hash for chain integrity."""
        parts = [
            previous_hash,
            timestamp_iso,
            action.value,
            json.dumps(target_ids, sort_keys=True),
            json.dumps(details, sort_keys=True, default=str),
        ]
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _append(self, entry: AuditEntry) -> None:
        """Append a single entry to the JSONL log file."""
        with open(self._log_file, "a", encoding="utf-8") as fh:
            fh.write(entry.model_dump_json() + "\n")

    def _read_last_hash(self) -> str:
        """Read the hash of the last entry in the log file, or return genesis."""
        if not os.path.exists(self._log_file):
            return _GENESIS_HASH
        try:
            last_line = ""
            with open(self._log_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    stripped = line.strip()
                    if stripped:
                        last_line = stripped
            if last_line:
                data = json.loads(last_line)
                return data.get("entry_hash", _GENESIS_HASH)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not read last audit hash: %s", exc)
        return _GENESIS_HASH

    # ------------------------------------------------------------------
    # Loading & verification
    # ------------------------------------------------------------------

    def load_from_file(self, path: str | None = None) -> list[AuditEntry]:
        """Load all audit entries from a JSONL log file.

        Parameters
        ----------
        path:
            Path to the JSONL file. Defaults to the instance's log file.

        Returns
        -------
        list[AuditEntry]
            All entries in chronological order.
        """
        log_file = path or self._log_file
        entries: list[AuditEntry] = []
        if not os.path.exists(log_file):
            return entries
        with open(log_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        entries.append(AuditEntry.model_validate_json(line))
                    except Exception as exc:
                        logger.warning("Skipping malformed audit entry: %s", exc)
        return entries

    @classmethod
    def verify_chain(cls, entries: list[AuditEntry]) -> tuple[bool, list[str]]:
        """Verify the hash-chain integrity of a sequence of audit entries.

        Recomputes each entry's hash using the same algorithm as ``log()``
        and checks that every ``previous_hash`` links to the preceding entry.

        Parameters
        ----------
        entries:
            The entries to verify, in chronological order.

        Returns
        -------
        tuple[bool, list[str]]
            ``(is_valid, error_messages)``
        """
        errors: list[str] = []
        if not entries:
            return True, []

        # First entry must reference the genesis hash
        if entries[0].previous_hash != _GENESIS_HASH:
            errors.append(
                f"First entry {entries[0].id} does not reference genesis hash "
                f"(got '{entries[0].previous_hash}')"
            )

        for i, entry in enumerate(entries):
            # Recompute the entry hash
            expected_hash = cls._compute_hash(
                previous_hash=entry.previous_hash,
                timestamp_iso=cls._normalize_timestamp(entry.timestamp),
                action=entry.action,
                target_ids=entry.target_ids,
                details=entry.details,
            )
            if entry.entry_hash != expected_hash:
                errors.append(
                    f"Entry {entry.id} hash mismatch: "
                    f"expected {expected_hash}, got {entry.entry_hash}"
                )

            # Check chain linkage (skip the first entry)
            if i > 0:
                if entry.previous_hash != entries[i - 1].entry_hash:
                    errors.append(
                        f"Entry {entry.id} chain broken: previous_hash={entry.previous_hash} "
                        f"does not match prior entry hash={entries[i - 1].entry_hash}"
                    )

        return len(errors) == 0, errors
