"""Unit tests for exporters."""

import json
import tempfile
from pathlib import Path

import pytest

from regulationcoder.models.evaluation import (
    ComplianceGap,
    ComplianceReport,
    EvaluationResult,
    RuleResult,
    RuleVerdict,
)


@pytest.fixture
def sample_report():
    return ComplianceReport(
        id="RPT-TEST-001",
        regulation_id="eu-ai-act-v1",
        system_name="Test System",
        provider_name="Test Corp",
        summary=EvaluationResult(
            total_rules=10,
            passed=7,
            failed=2,
            not_applicable=1,
            compliance_score=77.8,
        ),
        rule_results=[
            RuleResult(
                rule_id="RULE-001",
                requirement_id="REQ-001",
                title="Test Rule",
                verdict=RuleVerdict.PASS,
                article_ref="Article 10",
            ),
            RuleResult(
                rule_id="RULE-002",
                requirement_id="REQ-002",
                title="Failed Rule",
                verdict=RuleVerdict.FAIL,
                severity="critical",
                remediation="Fix this",
                article_ref="Article 15",
            ),
        ],
        critical_gaps=[
            ComplianceGap(
                rule_id="RULE-002",
                requirement_id="REQ-002",
                description="Missing metrics",
                severity="critical",
                remediation="Add disaggregated metrics",
                article_ref="Article 15",
            )
        ],
        overall_verdict="partial_compliance",
    )


class TestJsonExporter:
    def test_export(self, sample_report):
        from regulationcoder.exporters.json_exporter import export_report_json

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            path = f.name
        export_report_json(sample_report, path)
        with open(path) as f:
            data = json.load(f)
        assert data["id"] == "RPT-TEST-001"
        assert data["summary"]["compliance_score"] == 77.8


class TestHtmlExporter:
    def test_export(self, sample_report):
        from regulationcoder.exporters.html_exporter import export_report_html

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
            path = f.name
        export_report_html(sample_report, path)
        with open(path) as f:
            html = f.read()
        assert "Test System" in html
        assert "77.8" in html
        assert "DISCLAIMER" in html
