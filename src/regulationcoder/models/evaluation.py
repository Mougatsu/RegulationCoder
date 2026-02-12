"""Evaluation and compliance report models."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from regulationcoder.models.citation import Citation


class RuleVerdict(str, Enum):
    """Result of evaluating a single rule."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    MANUAL_REVIEW = "manual_review"


class RuleResult(BaseModel):
    """Result of evaluating a single compliance rule."""

    rule_id: str
    requirement_id: str
    title: str
    verdict: RuleVerdict
    severity: str = "medium"
    details: str = ""
    remediation: str = ""
    article_ref: str = ""
    citations: list[Citation] = Field(default_factory=list)


class ComplianceGap(BaseModel):
    """A gap identified in compliance evaluation."""

    rule_id: str
    requirement_id: str
    description: str
    severity: str
    remediation: str
    article_ref: str
    citations: list[Citation] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    """Summary statistics for a compliance evaluation."""

    total_rules: int = 0
    passed: int = 0
    failed: int = 0
    not_applicable: int = 0
    manual_review: int = 0
    compliance_score: float = 0.0


class ComplianceReport(BaseModel):
    """Full compliance evaluation report."""

    id: str = Field(..., description="Report ID")
    regulation_id: str
    regulation_version: str = ""
    system_name: str
    provider_name: str
    evaluation_date: datetime = Field(default_factory=datetime.utcnow)
    summary: EvaluationResult = Field(default_factory=EvaluationResult)
    rule_results: list[RuleResult] = Field(default_factory=list)
    critical_gaps: list[ComplianceGap] = Field(default_factory=list)
    high_gaps: list[ComplianceGap] = Field(default_factory=list)
    medium_gaps: list[ComplianceGap] = Field(default_factory=list)
    overall_verdict: str = "non_compliant"
    disclaimer: str = (
        "DISCLAIMER: This report is an engineering interpretation of regulatory requirements. "
        "It does not constitute legal advice. Consult qualified legal professionals for "
        "authoritative compliance determinations."
    )

    @property
    def compliance_score(self) -> float:
        return self.summary.compliance_score

    def export_json(self, path: str) -> None:
        """Export report as JSON file."""
        from regulationcoder.exporters.json_exporter import export_report_json

        export_report_json(self, path)

    def export_html(self, path: str) -> None:
        """Export report as HTML file."""
        from regulationcoder.exporters.html_exporter import export_report_html

        export_report_html(self, path)
