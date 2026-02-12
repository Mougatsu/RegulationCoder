#!/usr/bin/env python3
"""Generate the TalentScreen AI demo profile and save it as a JSON fixture.

TalentScreen AI is a fictional high-risk AI system for employment/recruitment
(Annex III, Section 4(a) of the EU AI Act).  It is mostly compliant but has
specific gaps intended to demonstrate the RegulationCoder evaluation pipeline.

Expected evaluation results (~53 rules):
  - Score:          ~78 / 100
  - Passed:         ~40
  - Failed:         ~11
  - Not Applicable: ~2

Key compliance gaps:
  - Missing disaggregated performance metrics (Article 15)
  - Missing automation bias safeguards (Article 14)
  - Missing foreseeable misuse documentation (Article 9)
  - Incomplete Annex IV technical documentation (Article 11)
  - Logging standards not met (Article 12)
  - Missing data preprocessing documentation (Article 10)
  - Other medium-severity gaps
"""

import json
import os
import sys

# Ensure the src directory is on the path when running as a script
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

from regulationcoder.models.profile import BiasExaminationReport, SystemProfile


def build_talentscreen_profile() -> SystemProfile:
    """Construct the TalentScreen AI system profile."""
    return SystemProfile(
        # --- Identity ---
        system_name="TalentScreen AI",
        provider_name="TalentTech GmbH",
        provider_jurisdiction="Germany",
        system_version="2.3.1",
        intended_purpose=(
            "Automated screening and ranking of job applicants based on CV analysis, "
            "skills matching and structured interview assessment for enterprise "
            "recruitment workflows."
        ),
        # --- Risk classification ---
        is_high_risk=True,
        high_risk_category="Employment, workers management and access to self-employment",
        annex_iii_section="Section 4(a)",

        # --- Article 10 - Data and Data Governance ---
        uses_training_data=True,
        dataset_names=[
            "recruitment-corpus-eu-v3",
            "interview-transcripts-anon-v2",
            "skills-taxonomy-esco-2024",
        ],
        bias_examination_report=BiasExaminationReport(
            covers_health_safety=True,
            covers_fundamental_rights=True,
            covers_prohibited_discrimination=True,
            datasets_examined=[
                "recruitment-corpus-eu-v3",
                "interview-transcripts-anon-v2",
            ],
            methodology="Demographic parity, equalized odds, and disparate impact analysis across protected groups",
            findings_summary=(
                "Minor disparities detected for age 55+ group in initial screening; "
                "mitigated via re-weighting and threshold adjustment."
            ),
        ),
        data_governance_practices_documented=True,
        training_data_relevance_documented=True,
        data_collection_process_documented=True,

        # --- Article 11 - Technical Documentation ---
        technical_documentation_exists=True,
        technical_documentation_url="https://docs.talenttech.eu/talentscreen/v2.3/technical-docs",

        # --- Article 12 - Record-Keeping ---
        automatic_logging_enabled=True,
        logging_capabilities=[
            "Input/output decision logging for every candidate evaluation",
            "Risk event and anomaly detection alerts",
            "Operational monitoring dashboard with real-time metrics",
            "Decision audit trail with full provenance",
        ],

        # --- Article 13 - Transparency ---
        instructions_for_use_provided=True,
        intended_purpose_documented=True,
        limitations_documented=True,

        # --- Article 14 - Human Oversight ---
        human_oversight_measures=[
            "Mandatory HR reviewer approval for all rejection decisions",
            "Escalation workflow for edge-case candidates",
            "Real-time monitoring dashboard for recruitment managers",
        ],
        human_can_override=True,
        human_can_interrupt=True,
        # INTENTIONAL GAP: No automation bias safeguards
        automation_bias_safeguards=[],

        # --- Article 15 - Accuracy, Robustness, Cybersecurity ---
        accuracy_metrics_documented=True,
        accuracy_levels_declared="Precision: 0.91, Recall: 0.88, F1: 0.895 (evaluated on held-out EU recruitment dataset Q4 2025)",
        # INTENTIONAL GAP: No disaggregated metrics
        disaggregated_performance_metrics=False,
        robustness_measures=[
            "Input validation and schema enforcement",
            "Graceful degradation with fallback to manual review on model errors",
            "Automated data drift detection with alerting",
        ],
        cybersecurity_measures=[
            "TLS 1.3 encryption for all data in transit",
            "AES-256 encryption for data at rest",
            "Role-based access control with SSO integration",
            "Annual penetration testing by external auditor",
        ],
        adversarial_testing_performed=True,

        # --- Article 9 - Risk Management ---
        risk_management_system_established=True,
        risk_management_continuous=True,
        residual_risks_documented=True,
        risk_mitigation_measures=[
            "Human-in-the-loop for all final hiring decisions",
            "Quarterly bias audits by independent third party",
            "Candidate appeal mechanism with human review",
        ],
        testing_procedures_documented=True,

        # --- Extra evidence fields ---
        extra={
            # Article 9 extras
            "foreseeable_misuse_documented": False,              # INTENTIONAL GAP
            "risk_measures_interaction_assessed": False,          # INTENTIONAL GAP
            "testing_metrics_defined": False,                     # INTENTIONAL GAP

            # Article 10 extras
            "data_preprocessing_documented": False,               # INTENTIONAL GAP
            "data_representativeness_documented": True,
            "processes_special_category_data": False,             # -> N/A for special data rule
            "special_data_safeguards_in_place": False,

            # Article 11 extras
            "technical_documentation_up_to_date": True,
            "techdoc_demonstrates_compliance": True,
            "techdoc_available_to_authorities": True,
            "techdoc_contains_annex_iv_elements": False,          # INTENTIONAL GAP
            "techdoc_clear_and_comprehensive": True,

            # Article 12 extras
            "logging_conforms_to_standards": False,               # INTENTIONAL GAP
            "post_market_monitoring_supported": False,            # INTENTIONAL GAP

            # Article 13 extras
            "system_operation_transparent": False,                 # INTENTIONAL GAP
            "oversight_documented_in_instructions": True,

            # Article 14 extras
            "output_interpretation_tools": True,

            # Article 15 extras
            "continuous_learning": False,                          # -> N/A for feedback loop rule
            "feedback_loop_mitigation": False,
        },
    )


def main() -> None:
    profile = build_talentscreen_profile()

    # Write JSON fixture
    fixture_dir = os.path.join(_PROJECT_ROOT, "tests", "fixtures")
    os.makedirs(fixture_dir, exist_ok=True)
    fixture_path = os.path.join(fixture_dir, "talentscreen_profile.json")

    with open(fixture_path, "w", encoding="utf-8") as fh:
        json.dump(profile.model_dump(mode="json"), fh, indent=2, ensure_ascii=False, default=str)

    print(f"TalentScreen AI profile saved to: {fixture_path}")
    print(f"  System:      {profile.system_name}")
    print(f"  Provider:    {profile.provider_name}")
    print(f"  High-risk:   {profile.is_high_risk}")
    print(f"  Category:    {profile.high_risk_category}")
    print(f"  Annex III:   {profile.annex_iii_section}")
    print(f"  Datasets:    {len(profile.dataset_names)}")
    print(f"  Extra fields: {len(profile.extra)}")


if __name__ == "__main__":
    main()
