"""Requirement model extracted from regulation clauses."""

from enum import Enum

from pydantic import BaseModel, Field

from regulationcoder.models.citation import Citation


class Modality(str, Enum):
    """Obligation modality extracted from legal text."""

    MUST = "must"
    MUST_NOT = "must_not"
    SHOULD = "should"
    SHOULD_NOT = "should_not"
    MAY = "may"


class Condition(BaseModel):
    """A condition or prerequisite for a requirement."""

    description: str
    clause_reference: str | None = None


class Requirement(BaseModel):
    """A structured requirement extracted from a regulation clause."""

    id: str = Field(..., description="Requirement ID, e.g. REQ-EU-AI-ACT-010-02F-001")
    clause_id: str = Field(..., description="Source clause ID")
    modality: Modality = Field(..., description="Obligation level")
    subject: str = Field(..., description="Who must comply")
    action: str = Field(..., description="What must be done")
    object: str = Field(..., description="What the action applies to")
    conditions: list[Condition] = Field(default_factory=list, description="Preconditions")
    exceptions: list[Condition] = Field(default_factory=list, description="Exceptions")
    scope: str = Field(default="", description="Applicability scope")
    jurisdiction: str = Field(default="European Union")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Extraction confidence")
    ambiguity_notes: str = Field(default="", description="Notes on ambiguous language")
    citations: list[Citation] = Field(default_factory=list, description="Source citations")
