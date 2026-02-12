"""Evaluate router — run compliance evaluations and retrieve reports."""

import asyncio

from fastapi import APIRouter, Body, HTTPException, Request

from regulationcoder.core.ai_analyzer import ComplianceAnalyzer
from regulationcoder.core.config import get_settings
from regulationcoder.core.engine import ComplianceEngine
from regulationcoder.models.ai_analysis import AIAnalysisResponse
from regulationcoder.models.evaluation import ComplianceReport
from regulationcoder.models.profile import SystemProfile

router = APIRouter(prefix="/api/evaluate", tags=["evaluate"])

_EXAMPLE_PROFILE = {
    "system_name": "TalentScreen AI",
    "provider_name": "TalentTech GmbH",
    "provider_jurisdiction": "Germany",
    "system_version": "2.1.0",
    "intended_purpose": "Automated screening and ranking of job applicants",
    "is_high_risk": True,
    "high_risk_category": "Employment, workers management and access to self-employment",
    "annex_iii_section": "4(a)",
    "uses_training_data": True,
    "dataset_names": ["applicant_training_v3", "applicant_validation_v3", "applicant_test_v3"],
    "bias_examination_report": {
        "covers_health_safety": True,
        "covers_fundamental_rights": True,
        "covers_prohibited_discrimination": True,
        "datasets_examined": ["applicant_training_v3", "applicant_validation_v3", "applicant_test_v3"],
    },
    "data_governance_practices_documented": True,
    "training_data_relevance_documented": True,
    "data_collection_process_documented": True,
    "technical_documentation_exists": True,
    "automatic_logging_enabled": True,
    "logging_capabilities": ["input_logging", "output_logging", "event_logging"],
    "instructions_for_use_provided": True,
    "intended_purpose_documented": True,
    "limitations_documented": True,
    "human_oversight_measures": ["human_review_of_decisions", "appeal_mechanism"],
    "human_can_override": True,
    "human_can_interrupt": True,
    "automation_bias_safeguards": [],
    "accuracy_metrics_documented": True,
    "accuracy_levels_declared": "Precision: 0.82, Recall: 0.78, F1: 0.80",
    "disaggregated_performance_metrics": False,
    "robustness_measures": ["input_validation", "adversarial_testing"],
    "cybersecurity_measures": ["encryption_at_rest", "encryption_in_transit", "access_control"],
    "adversarial_testing_performed": True,
    "risk_management_system_established": True,
    "risk_management_continuous": True,
    "residual_risks_documented": True,
    "risk_mitigation_measures": ["bias_mitigation", "human_oversight", "monitoring"],
    "testing_procedures_documented": True,
}


@router.post("/", response_model=ComplianceReport)
async def evaluate_profile(
    profile: SystemProfile = Body(..., openapi_examples={"TalentScreen AI (demo)": {"summary": "TalentScreen AI - recruitment system (partial compliance expected)", "value": _EXAMPLE_PROFILE}}),
    request: Request = None,
):
    """Evaluate a system profile against the regulation.

    Accepts a SystemProfile JSON body and returns a full ComplianceReport
    including per-rule verdicts, compliance gaps, and an overall score.
    """
    store = request.app.state.store

    # Use the default EU AI Act regulation
    engine = ComplianceEngine(regulation="eu-ai-act-v1")
    report = engine.evaluate(profile)

    # Store the report for later retrieval
    store["reports"][report.id] = report

    return report


@router.post("/ai-analysis", response_model=AIAnalysisResponse)
async def ai_analysis(
    profile: SystemProfile = Body(..., openapi_examples={"TalentScreen AI (demo)": {"summary": "TalentScreen AI - recruitment system (partial compliance expected)", "value": _EXAMPLE_PROFILE}}),
    request: Request = None,
):
    """Evaluate a system profile and get AI-powered analysis from Claude Opus 4.6.

    Runs the deterministic compliance engine first, then sends the profile
    and report to the ComplianceAnalyzer for deeper AI analysis including
    plain-language explanations and prioritised recommendations.
    """
    settings = get_settings()
    store = request.app.state.store

    # Step 1 — deterministic evaluation
    engine = ComplianceEngine(regulation="eu-ai-act-v1")
    report = engine.evaluate(profile)

    # Step 2 — store the report
    store["reports"][report.id] = report

    # Step 3 — AI analysis via Claude Opus 4.6 (run in thread to not block event loop)
    try:
        analyzer = ComplianceAnalyzer(settings)
        analysis = await asyncio.to_thread(analyzer.analyze, profile, report)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"AI analysis unavailable: {exc}",
        ) from exc

    # Step 4 — combined response
    return AIAnalysisResponse(
        report_id=report.id,
        system_name=report.system_name,
        provider_name=report.provider_name,
        compliance_score=report.compliance_score,
        overall_verdict=report.overall_verdict,
        analysis=analysis,
    )


@router.get("/reports", response_model=list[ComplianceReport])
async def list_reports(request: Request):
    """List all previously generated compliance reports."""
    store = request.app.state.store
    return list(store["reports"].values())


@router.get("/reports/{report_id}", response_model=ComplianceReport)
async def get_report(report_id: str, request: Request):
    """Get a specific compliance report by ID."""
    store = request.app.state.store
    report = store["reports"].get(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found")
    return report
