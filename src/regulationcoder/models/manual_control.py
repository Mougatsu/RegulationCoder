"""ManualControl model for requirements that need human verification."""

from enum import Enum

from pydantic import BaseModel, Field

from regulationcoder.models.citation import Citation


class EvidenceStatus(str, Enum):
    """Status of evidence collection for a manual control."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    REJECTED = "rejected"


class ManualControl(BaseModel):
    """A compliance control requiring manual/human verification."""

    id: str = Field(..., description="Control ID, e.g. CTRL-EU-AI-ACT-010-02F-001")
    rule_id: str = Field(..., description="Associated rule ID")
    requirement_id: str = Field(..., description="Source requirement ID")
    title: str = Field(..., description="Control title")
    description: str = Field(..., description="What the assessor must verify")
    verification_steps: list[str] = Field(default_factory=list, description="Steps for manual verification")
    evidence_required: list[str] = Field(default_factory=list, description="Required evidence artifacts")
    evidence_status: EvidenceStatus = Field(default=EvidenceStatus.NOT_STARTED)
    assessor_notes: str = Field(default="")
    citations: list[Citation] = Field(default_factory=list)
