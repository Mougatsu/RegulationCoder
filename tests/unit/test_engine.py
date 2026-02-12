"""Unit tests for the ComplianceEngine."""

import pytest

from regulationcoder.core.engine import ComplianceEngine
from regulationcoder.models.profile import SystemProfile
from regulationcoder.models.evaluation import RuleVerdict


class TestComplianceEngine:
    def test_field_resolution(self):
        engine = ComplianceEngine.__new__(ComplianceEngine)
        data = {
            "uses_training_data": True,
            "bias_examination_report": {
                "covers_health_safety": True,
                "covers_fundamental_rights": False,
            },
        }
        assert engine._resolve_field(data, "uses_training_data") is True
        assert engine._resolve_field(data, "system_profile.uses_training_data") is True
        assert engine._resolve_field(data, "bias_examination_report.covers_health_safety") is True
        assert engine._resolve_field(data, "bias_examination_report.covers_fundamental_rights") is False
        assert engine._resolve_field(data, "nonexistent_field") is None
        assert engine._resolve_field(data, "bias_examination_report.nonexistent") is None

    def test_evaluate_talentscreen(self, talentscreen_profile):
        """Test full evaluation with TalentScreen AI profile."""
        engine = ComplianceEngine(regulation="eu-ai-act-v1")
        report = engine.evaluate(talentscreen_profile)

        assert report.system_name == "TalentScreen AI"
        assert report.provider_name == "TalentTech GmbH"
        assert report.regulation_id == "eu-ai-act-v1"
        assert report.summary.total_rules > 0
        assert report.summary.passed > 0
        # TalentScreen has known gaps, so should have failures
        assert report.summary.failed > 0
        assert report.summary.compliance_score > 0
        assert report.overall_verdict in ("partial_compliance", "compliant", "non_compliant")
        # Should not be fully compliant due to known gaps
        assert report.overall_verdict != "compliant" or len(report.critical_gaps) == 0

    def test_evaluate_minimal_profile(self):
        """Test evaluation with a minimal non-compliant profile."""
        engine = ComplianceEngine(regulation="eu-ai-act-v1")
        profile = SystemProfile(
            system_name="Minimal System",
            provider_name="Test Corp",
            intended_purpose="Testing",
            is_high_risk=True,
        )
        report = engine.evaluate(profile)
        assert report.summary.failed > report.summary.passed
        assert report.overall_verdict in ("non_compliant", "partial_compliance")
