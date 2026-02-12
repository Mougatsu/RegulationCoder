"""SystemProfile model representing an AI system being evaluated for compliance."""

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class BiasExaminationReport(BaseModel):
    """Documented bias examination results."""

    covers_health_safety: bool = False
    covers_fundamental_rights: bool = False
    covers_prohibited_discrimination: bool = False
    datasets_examined: list[str] = Field(default_factory=list)
    examination_date: date | None = None
    methodology: str = ""
    findings_summary: str = ""


class SystemProfile(BaseModel):
    """Profile of an AI system being evaluated for regulatory compliance."""

    system_name: str = Field(..., description="Name of the AI system")
    provider_name: str = Field(..., description="Organization providing the system")
    provider_jurisdiction: str = Field(default="")
    system_version: str = Field(default="1.0.0")
    intended_purpose: str = Field(..., description="Intended purpose of the AI system")
    is_high_risk: bool = Field(default=False)
    high_risk_category: str = Field(default="")
    annex_iii_section: str = Field(default="")

    # Data & Training (Article 10)
    uses_training_data: bool = Field(default=False)
    dataset_names: list[str] = Field(default_factory=list)
    bias_examination_report: BiasExaminationReport | None = None
    data_governance_practices_documented: bool = Field(default=False)
    training_data_relevance_documented: bool = Field(default=False)
    data_collection_process_documented: bool = Field(default=False)

    # Technical Documentation (Article 11)
    technical_documentation_exists: bool = Field(default=False)
    technical_documentation_url: str = Field(default="")

    # Record-keeping (Article 12)
    automatic_logging_enabled: bool = Field(default=False)
    logging_capabilities: list[str] = Field(default_factory=list)

    # Transparency (Article 13)
    instructions_for_use_provided: bool = Field(default=False)
    intended_purpose_documented: bool = Field(default=False)
    limitations_documented: bool = Field(default=False)

    # Human oversight (Article 14)
    human_oversight_measures: list[str] = Field(default_factory=list)
    human_can_override: bool = Field(default=False)
    human_can_interrupt: bool = Field(default=False)
    automation_bias_safeguards: list[str] = Field(default_factory=list)

    # Accuracy, Robustness, Cybersecurity (Article 15)
    accuracy_metrics_documented: bool = Field(default=False)
    accuracy_levels_declared: str = Field(default="")
    disaggregated_performance_metrics: bool = Field(default=False)
    robustness_measures: list[str] = Field(default_factory=list)
    cybersecurity_measures: list[str] = Field(default_factory=list)
    adversarial_testing_performed: bool = Field(default=False)

    # Risk Management (Article 9)
    risk_management_system_established: bool = Field(default=False)
    risk_management_continuous: bool = Field(default=False)
    residual_risks_documented: bool = Field(default=False)
    risk_mitigation_measures: list[str] = Field(default_factory=list)
    testing_procedures_documented: bool = Field(default=False)

    # Extra evidence fields
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional profile fields")
