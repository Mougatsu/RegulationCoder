"""Unit tests for the audit module."""

import json
import tempfile
from pathlib import Path

import pytest

from regulationcoder.models.audit_entry import AuditAction


class TestAuditLogger:
    def test_log_and_chain(self):
        from regulationcoder.audit.logger import AuditLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(tmpdir)

            entry1 = logger.log(
                action=AuditAction.INGEST,
                stage="ingestion",
                target_ids=["file1.pdf"],
                details={"length": 1000},
            )
            assert entry1.entry_hash != ""
            assert entry1.previous_hash == "0" * 64  # genesis hash

            entry2 = logger.log(
                action=AuditAction.PARSE,
                stage="parsing",
                target_ids=["clause1", "clause2"],
                details={"count": 2},
            )
            assert entry2.previous_hash == entry1.entry_hash
            assert entry2.entry_hash != entry1.entry_hash

    def test_verify_chain(self):
        from regulationcoder.audit.logger import AuditLogger
        from regulationcoder.audit.chain import AuditChainVerifier

        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(tmpdir)
            logger.log(action=AuditAction.INGEST, stage="s1", target_ids=["a"])
            logger.log(action=AuditAction.PARSE, stage="s2", target_ids=["b"])
            logger.log(action=AuditAction.EXTRACT, stage="s3", target_ids=["c"])

            verifier = AuditChainVerifier()
            is_valid, errors = verifier.verify(tmpdir)
            assert is_valid is True
            assert len(errors) == 0
