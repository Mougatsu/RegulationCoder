"""JudgeReport model for Anthropic judge gate outputs."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    """Judge verdict for a gate evaluation."""

    APPROVE = "approve"
    REVISE = "revise"
    BLOCK = "block"


class FindingSeverity(str, Enum):
    """Severity of a judge finding."""

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class FindingType(str, Enum):
    """Type of judge finding."""

    HALLUCINATION = "hallucination"
    MODALITY_ERROR = "modality_error"
    SUBJECT_ERROR = "subject_error"
    OMISSION = "omission"
    AMBIGUITY = "ambiguity"
    LOGIC_ERROR = "logic_error"
    COVERAGE_GAP = "coverage_gap"
    SYNTAX_ERROR = "syntax_error"
    CODE_FIDELITY = "code_fidelity"
    IMPACT_MISSED = "impact_missed"


class JudgeScores(BaseModel):
    """Scoring rubric for all judge gates."""

    grounding_score: float = Field(0.0, ge=0.0, le=1.0, description="Citation coverage")
    hallucination_risk: float = Field(0.0, ge=0.0, le=1.0, description="Risk of fabricated content")
    ambiguity_score: float = Field(0.0, ge=0.0, le=1.0, description="Remaining ambiguity")
    implementability_score: float = Field(0.0, ge=0.0, le=1.0, description="Feasibility to implement")
    test_adequacy_score: float = Field(0.0, ge=0.0, le=1.0, description="Test coverage quality")
    overall_confidence: float = Field(0.0, ge=0.0, le=1.0)


class Finding(BaseModel):
    """A specific finding from a judge evaluation."""

    finding_type: FindingType
    severity: FindingSeverity
    description: str
    affected_field: str = ""
    suggested_fix: str = ""


class JudgeReport(BaseModel):
    """Output from an Anthropic judge gate evaluation."""

    id: str = Field(..., description="Report ID")
    stage: str = Field(..., description="Gate stage: gate_a_extraction, gate_b_formalization, etc.")
    target_ids: list[str] = Field(default_factory=list, description="IDs of items being judged")
    verdict: Verdict = Field(..., description="Overall verdict")
    scores: JudgeScores = Field(default_factory=JudgeScores)
    findings: list[Finding] = Field(default_factory=list)
    required_fixes: list[str] = Field(default_factory=list)
    citations_checked: list[str] = Field(default_factory=list)
    model_used: str = Field(default="claude-opus-4-6")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
