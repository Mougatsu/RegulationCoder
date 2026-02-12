"""Citation model for tracing back to source regulation text."""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """Reference to a specific location in a regulation document."""

    clause_id: str = Field(..., description="Deterministic clause ID, e.g. eu-ai-act-v1/art10/para2/sub-f")
    article_ref: str = Field(..., description="Human-readable article reference, e.g. 'Article 10'")
    paragraph_ref: str | None = Field(None, description="Paragraph number as string")
    subsection_ref: str | None = Field(None, description="Subsection letter")
    page_number: int | None = Field(None, description="Page number in source document")
    exact_quote: str = Field(..., description="Exact quoted text from the source")
