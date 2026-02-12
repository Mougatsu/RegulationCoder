"""Regulation model representing a complete regulation document."""

from datetime import datetime

from pydantic import BaseModel, Field


class Regulation(BaseModel):
    """A regulation document that has been ingested."""

    id: str = Field(..., description="Regulation identifier, e.g. eu-ai-act")
    title: str = Field(..., description="Full title of the regulation")
    short_name: str = Field(..., description="Short name, e.g. 'EU AI Act'")
    document_version: str = Field(..., description="Version identifier")
    jurisdiction: str = Field(default="European Union")
    language: str = Field(default="en")
    source_url: str | None = Field(None, description="Original source URL")
    source_file: str | None = Field(None, description="Path to ingested source file")
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
    total_articles: int = Field(default=0)
    total_clauses: int = Field(default=0)
