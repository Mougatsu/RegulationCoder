"""Shared test fixtures for RegulationCoder."""

import json
import pytest
from pathlib import Path

from regulationcoder.models.citation import Citation
from regulationcoder.models.clause import Clause
from regulationcoder.models.requirement import Condition, Modality, Requirement
from regulationcoder.models.rule import Rule, RuleType, Severity, TestCase
from regulationcoder.models.profile import BiasExaminationReport, SystemProfile


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_clause() -> Clause:
    return Clause(
        id="eu-ai-act-v1/art10/para2/sub-f",
        regulation_id="eu-ai-act",
        document_version="2024-1689-oj",
        article_number=10,
        paragraph_number=2,
        subsection_letter="f",
        text=(
            "examination in view of possible biases that are likely to affect "
            "the health and safety of persons, have a negative impact on "
            "fundamental rights or lead to discrimination prohibited under "
            "Union law, especially where data outputs influence inputs for "
            "future operations"
        ),
        language="en",
        page_ref=48,
        parent_clause_id="eu-ai-act-v1/art10/para2",
    )


@pytest.fixture
def sample_citation() -> Citation:
    return Citation(
        clause_id="eu-ai-act-v1/art10/para2/sub-f",
        article_ref="Article 10",
        paragraph_ref="2",
        subsection_ref="f",
        page_number=48,
        exact_quote=(
            "examination in view of possible biases that are likely to affect "
            "the health and safety of persons..."
        ),
    )


@pytest.fixture
def sample_requirement(sample_citation) -> Requirement:
    return Requirement(
        id="REQ-EU-AI-ACT-010-02F-001",
        clause_id="eu-ai-act-v1/art10/para2/sub-f",
        modality=Modality.MUST,
        subject="provider of high-risk AI system",
        action="examine training, validation and testing datasets",
        object=(
            "possible biases that are likely to affect health and safety of "
            "persons, have negative impact on fundamental rights, or lead to "
            "discrimination prohibited under Union law"
        ),
        conditions=[
            Condition(
                description="The high-risk AI system makes use of techniques involving training of AI models with data",
                clause_reference="eu-ai-act-v1/art10/para1",
            )
        ],
        exceptions=[
            Condition(
                description="For systems not using training techniques, applies only to testing datasets",
                clause_reference="eu-ai-act-v1/art10/para6",
            )
        ],
        scope="High-risk AI systems as classified under Article 6",
        jurisdiction="European Union",
        confidence=0.95,
        ambiguity_notes="The phrase 'likely to affect' introduces a probability threshold that is not quantified.",
        citations=[sample_citation],
    )


@pytest.fixture
def sample_rule(sample_citation) -> Rule:
    return Rule(
        id="RULE-EU-AI-ACT-010-02F-001",
        requirement_id="REQ-EU-AI-ACT-010-02F-001",
        rule_type=RuleType.SEMI_AUTOMATED,
        title="Dataset Bias Examination",
        description="Verify that bias examination has been conducted for all datasets.",
        inputs_needed=[
            "system_profile.uses_training_data",
            "system_profile.bias_examination_report",
            "system_profile.bias_examination_report.covers_health_safety",
            "system_profile.bias_examination_report.covers_fundamental_rights",
            "system_profile.bias_examination_report.covers_prohibited_discrimination",
            "system_profile.bias_examination_report.datasets_examined",
            "system_profile.dataset_names",
        ],
        evaluation_logic=(
            "if not uses_training_data: result = 'not_applicable'\n"
            "elif not bias_examination_report: result = 'fail'\n"
            "elif not all([covers_health_safety, covers_fundamental_rights, covers_prohibited_discrimination]): result = 'fail'\n"
            "elif set(datasets_examined) != set(dataset_names): result = 'fail'\n"
            "else: result = 'pass'"
        ),
        severity=Severity.CRITICAL,
        remediation=(
            "Conduct and document a comprehensive bias examination covering "
            "health/safety, fundamental rights, and prohibited discrimination "
            "for all datasets."
        ),
        test_cases=[
            TestCase(
                id="TC-001",
                description="Complete report covering all areas",
                input_data={
                    "uses_training_data": True,
                    "bias_examination_report": {
                        "covers_health_safety": True,
                        "covers_fundamental_rights": True,
                        "covers_prohibited_discrimination": True,
                        "datasets_examined": ["ds1"],
                    },
                    "dataset_names": ["ds1"],
                },
                expected_result="pass",
            ),
            TestCase(
                id="TC-002",
                description="Missing report",
                input_data={
                    "uses_training_data": True,
                    "bias_examination_report": None,
                    "dataset_names": ["ds1"],
                },
                expected_result="fail",
            ),
            TestCase(
                id="TC-003",
                description="No training data used",
                input_data={"uses_training_data": False},
                expected_result="not_applicable",
            ),
        ],
        citations=[sample_citation],
    )


@pytest.fixture
def talentscreen_profile() -> SystemProfile:
    """TalentScreen AI demo profile — partial compliance expected."""
    return SystemProfile(
        system_name="TalentScreen AI",
        provider_name="TalentTech GmbH",
        provider_jurisdiction="Germany",
        system_version="2.1.0",
        intended_purpose="Automated screening and ranking of job applicants",
        is_high_risk=True,
        high_risk_category="Employment, workers management and access to self-employment",
        annex_iii_section="4(a)",
        uses_training_data=True,
        dataset_names=[
            "applicant_training_v3",
            "applicant_validation_v3",
            "applicant_test_v3",
        ],
        bias_examination_report=BiasExaminationReport(
            covers_health_safety=True,
            covers_fundamental_rights=True,
            covers_prohibited_discrimination=True,
            datasets_examined=[
                "applicant_training_v3",
                "applicant_validation_v3",
                "applicant_test_v3",
            ],
        ),
        data_governance_practices_documented=True,
        training_data_relevance_documented=True,
        data_collection_process_documented=True,
        technical_documentation_exists=True,
        automatic_logging_enabled=True,
        logging_capabilities=["input_logging", "output_logging", "event_logging"],
        instructions_for_use_provided=True,
        intended_purpose_documented=True,
        limitations_documented=True,
        human_oversight_measures=["human_review_of_decisions", "appeal_mechanism"],
        human_can_override=True,
        human_can_interrupt=True,
        automation_bias_safeguards=[],  # GAP: missing
        accuracy_metrics_documented=True,
        accuracy_levels_declared="Precision: 0.82, Recall: 0.78, F1: 0.80",
        disaggregated_performance_metrics=False,  # GAP: missing
        robustness_measures=["input_validation", "adversarial_testing"],
        cybersecurity_measures=["encryption_at_rest", "encryption_in_transit", "access_control"],
        adversarial_testing_performed=True,
        risk_management_system_established=True,
        risk_management_continuous=True,
        residual_risks_documented=True,
        risk_mitigation_measures=["bias_mitigation", "human_oversight", "monitoring"],
        testing_procedures_documented=True,
    )
