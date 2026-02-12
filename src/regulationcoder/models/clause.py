"""Clause model representing a segment of regulation text."""

from pydantic import BaseModel, Field


class Clause(BaseModel):
    """A single clause extracted from a regulation document."""

    id: str = Field(..., description="Deterministic ID, e.g. eu-ai-act-v1/art10/para2/sub-f")
    regulation_id: str = Field(..., description="Parent regulation identifier")
    document_version: str = Field(..., description="Document version, e.g. 2024-1689-oj")
    article_number: int = Field(..., description="Article number")
    paragraph_number: int | None = Field(None, description="Paragraph number within article")
    subsection_letter: str | None = Field(None, description="Subsection letter (a, b, c, ...)")
    text: str = Field(..., description="Full text of the clause")
    language: str = Field(default="en", description="ISO 639-1 language code")
    page_ref: int | None = Field(None, description="Page number in source document")
    parent_clause_id: str | None = Field(None, description="ID of the parent clause")
