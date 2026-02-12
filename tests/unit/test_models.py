"""Unit tests for Pydantic data models."""

import json
import pytest

from regulationcoder.models.citation import Citation
from regulationcoder.models.clause import Clause
from regulationcoder.models.requirement import Condition, Modality, Requirement
from regulationcoder.models.rule import Rule, RuleType, Severity, TestCase
from regulationcoder.models.profile import BiasExaminationReport, SystemProfile
from regulationcoder.models.evaluation import (
    ComplianceGap,
    ComplianceReport,
    EvaluationResult,
    RuleResult,
    RuleVerdict,
)
from regulationcoder.models.judge_report import (
    Finding,
    FindingSeverity,
    FindingType,
    JudgeReport,
    JudgeScores,
    Verdict,
)
from regulationcoder.models.audit_entry import AuditAction, AuditEntry
from regulationcoder.models.diff import ChangeType, ClauseChange, SemanticChangeType


class TestCitation:
    def test_create(self):
        c = Citation(
            clause_id="eu-ai-act-v1/art10/para2",
            article_ref="Article 10",
            exact_quote="some text",
        )
        assert c.clause_id == "eu-ai-act-v1/art10/para2"
        assert c.page_number is None

    def test_serialization(self):
        c = Citation(
            clause_id="test/art1",
            article_ref="Article 1",
            paragraph_ref="1",
            page_number=5,
            exact_quote="test quote",
        )
        data = c.model_dump()
        assert data["page_number"] == 5
        c2 = Citation.model_validate(data)
        assert c2 == c


class TestClause:
    def test_create(self, sample_clause):
        assert sample_clause.article_number == 10
        assert sample_clause.paragraph_number == 2
        assert sample_clause.subsection_letter == "f"
        assert sample_clause.language == "en"

    def test_id_format(self, sample_clause):
        assert sample_clause.id.startswith("eu-ai-act-v1/")
        assert "/art10/" in sample_clause.id


class TestRequirement:
    def test_modality_enum(self):
        assert Modality.MUST.value == "must"
        assert Modality.SHOULD.value == "should"
        assert Modality.MAY.value == "may"

    def test_create(self, sample_requirement):
        assert sample_requirement.modality == Modality.MUST
        assert len(sample_requirement.conditions) == 1
        assert len(sample_requirement.exceptions) == 1
        assert sample_requirement.confidence == 0.95

    def test_json_roundtrip(self, sample_requirement):
        json_str = sample_requirement.model_dump_json()
        data = json.loads(json_str)
        req2 = Requirement.model_validate(data)
        assert req2.id == sample_requirement.id
        assert req2.modality == sample_requirement.modality


class TestRule:
    def test_create(self, sample_rule):
        assert sample_rule.rule_type == RuleType.SEMI_AUTOMATED
        assert sample_rule.severity == Severity.CRITICAL
        assert len(sample_rule.test_cases) == 3

    def test_test_cases(self, sample_rule):
        tc = sample_rule.test_cases[0]
        assert tc.expected_result == "pass"
        assert tc.input_data["uses_training_data"] is True


class TestSystemProfile:
    def test_create(self, talentscreen_profile):
        p = talentscreen_profile
        assert p.system_name == "TalentScreen AI"
        assert p.is_high_risk is True
        assert p.uses_training_data is True
        assert len(p.dataset_names) == 3

    def test_known_gaps(self, talentscreen_profile):
        p = talentscreen_profile
        assert p.disaggregated_performance_metrics is False
        assert p.automation_bias_safeguards == []


class TestJudgeReport:
    def test_verdicts(self):
        assert Verdict.APPROVE.value == "approve"
        assert Verdict.REVISE.value == "revise"
        assert Verdict.BLOCK.value == "block"

    def test_create(self):
        report = JudgeReport(
            id="JUDGE-TEST-001",
            stage="gate_a_extraction",
            verdict=Verdict.APPROVE,
            scores=JudgeScores(
                grounding_score=0.95,
                hallucination_risk=0.05,
                overall_confidence=0.90,
            ),
        )
        assert report.verdict == Verdict.APPROVE
        assert report.scores.grounding_score == 0.95


class TestComplianceReport:
    def test_overall_verdict(self):
        report = ComplianceReport(
            id="RPT-TEST-001",
            regulation_id="eu-ai-act-v1",
            system_name="Test System",
            provider_name="Test Corp",
            summary=EvaluationResult(
                total_rules=10,
                passed=8,
                failed=2,
                compliance_score=80.0,
            ),
            overall_verdict="partial_compliance",
        )
        assert report.compliance_score == 80.0
        assert "DISCLAIMER" in report.disclaimer


class TestAuditEntry:
    def test_create(self):
        entry = AuditEntry(
            id="AUDIT-001",
            action=AuditAction.EXTRACT,
            stage="extraction",
            target_ids=["REQ-001"],
        )
        assert entry.action == AuditAction.EXTRACT
        assert entry.actor == "system"


class TestDiff:
    def test_clause_change(self):
        change = ClauseChange(
            clause_id="art10/para1",
            change_type=ChangeType.MODIFIED,
            semantic_type=SemanticChangeType.SUBSTANTIVE,
            old_text="old",
            new_text="new",
        )
        assert change.change_type == ChangeType.MODIFIED
