"""Rule model representing a machine-checkable compliance rule."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from regulationcoder.models.citation import Citation


class RuleType(str, Enum):
    """Type of compliance rule."""

    AUTOMATED = "automated"
    SEMI_AUTOMATED = "semi_automated"
    MANUAL = "manual"


class Severity(str, Enum):
    """Severity of non-compliance."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class TestCase(BaseModel):
    """A test case for validating rule evaluation logic."""

    id: str
    description: str
    input_data: dict[str, Any]
    expected_result: str  # "pass", "fail", "not_applicable"


class Rule(BaseModel):
    """A formalized compliance rule derived from a requirement."""

    id: str = Field(..., description="Rule ID, e.g. RULE-EU-AI-ACT-010-02F-001")
    requirement_id: str = Field(..., description="Source requirement ID")
    rule_type: RuleType = Field(..., description="Automation level")
    title: str = Field(..., description="Human-readable rule title")
    description: str = Field(default="", description="Detailed description")
    inputs_needed: list[str] = Field(default_factory=list, description="Required profile fields")
    evaluation_logic: str = Field(..., description="Pseudocode evaluation logic")
    severity: Severity = Field(default=Severity.MEDIUM)
    remediation: str = Field(default="", description="Remediation guidance")
    test_cases: list[TestCase] = Field(default_factory=list, description="Validation test cases")
    citations: list[Citation] = Field(default_factory=list, description="Source citations")
