"""AuditEntry model for immutable audit trail."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AuditAction(str, Enum):
    """Types of auditable actions."""

    INGEST = "ingest"
    PARSE = "parse"
    EXTRACT = "extract"
    FORMALIZE = "formalize"
    CODEGEN = "codegen"
    JUDGE = "judge"
    EVALUATE = "evaluate"
    DIFF = "diff"
    EXPORT = "export"


class AuditEntry(BaseModel):
    """An immutable, hash-chained audit log entry."""

    id: str = Field(..., description="Unique entry ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: AuditAction
    stage: str = Field(..., description="Pipeline stage")
    actor: str = Field(default="system", description="Who performed the action")
    target_ids: list[str] = Field(default_factory=list, description="IDs of affected items")
    input_hash: str = Field(default="", description="SHA-256 of input data")
    output_hash: str = Field(default="", description="SHA-256 of output data")
    previous_hash: str = Field(default="", description="Hash of previous audit entry (chain)")
    entry_hash: str = Field(default="", description="SHA-256 of this entry")
    details: dict[str, Any] = Field(default_factory=dict, description="Additional details")
    model_used: str = Field(default="")
    verdict: str = Field(default="")
