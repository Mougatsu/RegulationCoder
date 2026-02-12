"""AI Analysis models — structured output from Claude Opus 4.6 deep analysis."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AIInsight(BaseModel):
    """A single insight from the AI analysis."""

    category: str = Field(
        ..., description="Category: risk_assessment, data_governance, transparency, human_oversight, accuracy, etc."
    )
    title: str = Field(..., description="Short title for this insight")
    analysis: str = Field(..., description="Detailed analysis text")
    severity: str = Field(default="medium", description="critical, high, medium, low, info")
    recommendations: list[str] = Field(default_factory=list, description="Actionable recommendations")
    relevant_articles: list[str] = Field(default_factory=list, description="EU AI Act articles referenced")


class AIAnalysisResult(BaseModel):
    """Full AI analysis output from Claude Opus 4.6."""

    id: str = Field(..., description="Analysis ID")
    report_id: str = Field(..., description="ID of the compliance report this analysis is for")
    model_used: str = Field(default="claude-opus-4-6")
    executive_summary: str = Field(..., description="2-4 sentence executive summary")
    overall_risk_level: str = Field(
        default="medium", description="Overall risk: critical, high, medium, low"
    )
    risk_narrative: str = Field(
        ..., description="Narrative explanation of the overall risk posture"
    )
    key_strengths: list[str] = Field(default_factory=list, description="What the system does well")
    insights: list[AIInsight] = Field(default_factory=list, description="Detailed per-area insights")
    prioritized_actions: list[str] = Field(
        default_factory=list,
        description="Ordered list of recommended actions, highest priority first",
    )
    regulatory_context: str = Field(
        default="",
        description="Broader regulatory context and implications",
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AIAnalysisResponse(BaseModel):
    """Combined response with both deterministic report and AI analysis."""

    report_id: str
    system_name: str
    provider_name: str
    compliance_score: float
    overall_verdict: str
    analysis: AIAnalysisResult
