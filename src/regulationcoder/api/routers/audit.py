"""Audit router — query audit trail and verify hash-chain integrity."""

from datetime import datetime

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

from regulationcoder.audit.logger import AuditLogger
from regulationcoder.models.audit_entry import AuditAction, AuditEntry

router = APIRouter(prefix="/api/audit", tags=["audit"])


class AuditVerificationResult(BaseModel):
    """Result of an audit hash-chain verification."""
    is_valid: bool
    total_entries: int
    errors: list[str]
    first_entry_time: str | None = None
    last_entry_time: str | None = None


@router.get("/logs", response_model=list[AuditEntry])
async def list_audit_logs(
    request: Request,
    action: AuditAction | None = Query(None, description="Filter by action type"),
    stage: str | None = Query(None, description="Filter by pipeline stage"),
    actor: str | None = Query(None, description="Filter by actor"),
    since: datetime | None = Query(None, description="Only entries after this timestamp"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum entries to return"),
):
    """List audit log entries with optional filters.

    Entries are returned in reverse chronological order (most recent first).
    """
    store = request.app.state.store
    entries: list[AuditEntry] = list(store.get("audit_entries", []))

    # Also try loading from the default audit log file
    if not entries:
        try:
            audit_logger = AuditLogger(log_dir="./audit_logs")
            entries = audit_logger.load_from_file()
        except Exception:
            entries = []

    # Apply filters
    if action is not None:
        entries = [e for e in entries if e.action == action]
    if stage is not None:
        entries = [e for e in entries if e.stage == stage]
    if actor is not None:
        entries = [e for e in entries if e.actor == actor]
    if since is not None:
        entries = [e for e in entries if e.timestamp >= since]

    # Sort by timestamp descending and apply limit
    entries.sort(key=lambda e: e.timestamp, reverse=True)
    return entries[:limit]


@router.get("/verify", response_model=AuditVerificationResult)
async def verify_audit_chain(
    request: Request,
    log_dir: str = Query("./audit_logs", description="Directory containing audit log files"),
):
    """Verify the integrity of the audit log hash chain.

    This endpoint reads the JSONL audit log, recomputes each entry's hash,
    and verifies that every entry's ``previous_hash`` correctly references the
    preceding entry. Any tampered, missing, or reordered entries will be
    flagged.
    """
    try:
        audit_logger = AuditLogger(log_dir=log_dir)
        entries = audit_logger.load_from_file()
    except Exception as e:
        return AuditVerificationResult(
            is_valid=False,
            total_entries=0,
            errors=[f"Failed to load audit log: {str(e)}"],
        )

    if not entries:
        return AuditVerificationResult(
            is_valid=True,
            total_entries=0,
            errors=[],
        )

    is_valid, errors = AuditLogger.verify_chain(entries)

    return AuditVerificationResult(
        is_valid=is_valid,
        total_entries=len(entries),
        errors=errors,
        first_entry_time=entries[0].timestamp.isoformat(),
        last_entry_time=entries[-1].timestamp.isoformat(),
    )
