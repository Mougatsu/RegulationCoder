"""Integration tests for the full pipeline (no API calls required)."""

import json
from pathlib import Path

import pytest

from regulationcoder.core.engine import ComplianceEngine
from regulationcoder.models.profile import SystemProfile


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


class TestEndToEndEvaluation:
    """Test full evaluation pipeline with pre-built EU AI Act data."""

    def test_talentscreen_evaluation(self):
        """End-to-end: load profile, evaluate, verify expected score range."""
        profile_path = FIXTURES_DIR / "talentscreen_profile.json"
        with open(profile_path) as f:
            profile_data = json.load(f)

        profile = SystemProfile.model_validate(profile_data)
        engine = ComplianceEngine(regulation="eu-ai-act-v1")
        report = engine.evaluate(profile)

        # Verify report structure
        assert report.system_name == "TalentScreen AI"
        assert report.regulation_id == "eu-ai-act-v1"
        assert report.summary.total_rules > 0

        # TalentScreen should be partially compliant
        assert report.overall_verdict == "partial_compliance"
        assert 60 <= report.summary.compliance_score <= 95

        # Should have critical gaps for known missing items
        assert len(report.critical_gaps) > 0

        # Print summary for visibility
        print(f"\nScore: {report.summary.compliance_score}/100")
        print(f"Passed: {report.summary.passed}")
        print(f"Failed: {report.summary.failed}")
        print(f"N/A: {report.summary.not_applicable}")
        print(f"Critical gaps: {len(report.critical_gaps)}")
        for gap in report.critical_gaps:
            print(f"  - {gap.rule_id}: {gap.description}")

    def test_json_export(self, tmp_path):
        """Test that evaluation results can be exported to JSON."""
        profile = SystemProfile(
            system_name="Test System",
            provider_name="Test Corp",
            intended_purpose="Testing",
            is_high_risk=True,
        )
        engine = ComplianceEngine(regulation="eu-ai-act-v1")
        report = engine.evaluate(profile)

        output_path = str(tmp_path / "report.json")
        report.export_json(output_path)

        with open(output_path) as f:
            data = json.load(f)
        assert data["system_name"] == "Test System"
        assert "summary" in data

    def test_html_export(self, tmp_path):
        """Test that evaluation results can be exported to HTML."""
        profile = SystemProfile(
            system_name="Test System",
            provider_name="Test Corp",
            intended_purpose="Testing",
            is_high_risk=True,
        )
        engine = ComplianceEngine(regulation="eu-ai-act-v1")
        report = engine.evaluate(profile)

        output_path = str(tmp_path / "report.html")
        report.export_html(output_path)

        with open(output_path) as f:
            html = f.read()
        assert "Test System" in html

    def test_regulation_data_loaded(self):
        """Verify that EU AI Act data is properly loaded."""
        from regulationcoder.rules.eu_ai_act_v1 import (
            get_clauses,
            get_requirements,
            get_rules,
        )

        clauses = get_clauses()
        requirements = get_requirements()
        rules = get_rules()

        assert len(clauses) >= 30, f"Expected >=30 clauses, got {len(clauses)}"
        assert len(requirements) >= 30, f"Expected >=30 requirements, got {len(requirements)}"
        assert len(rules) >= 30, f"Expected >=30 rules, got {len(rules)}"

        # All rules should reference valid requirements
        req_ids = {r.id for r in requirements}
        for rule in rules:
            assert rule.requirement_id in req_ids, f"Rule {rule.id} references unknown req {rule.requirement_id}"
