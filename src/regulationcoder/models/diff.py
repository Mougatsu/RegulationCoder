"""Diff models for regulation version comparison."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ChangeType(str, Enum):
    """Type of change between regulation versions."""

    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


class SemanticChangeType(str, Enum):
    """Semantic classification of a change."""

    SUBSTANTIVE = "substantive"
    EDITORIAL = "editorial"
    STRUCTURAL = "structural"
    CLARIFICATION = "clarification"


class ClauseChange(BaseModel):
    """A change detected in a single clause."""

    clause_id: str
    change_type: ChangeType
    semantic_type: SemanticChangeType | None = None
    old_text: str = ""
    new_text: str = ""
    diff_summary: str = ""


class ImpactedItem(BaseModel):
    """An item impacted by a regulation change."""

    item_id: str
    item_type: str  # "requirement", "rule", "code"
    impact_description: str
    needs_regeneration: bool = False
    priority: str = "medium"


class RegulationDiff(BaseModel):
    """Diff between two versions of a regulation."""

    old_version: str
    new_version: str
    clause_changes: list[ClauseChange] = Field(default_factory=list)
    impacted_items: list[ImpactedItem] = Field(default_factory=list)


class DiffReport(BaseModel):
    """Full report of changes between regulation versions."""

    id: str
    regulation_id: str
    old_version: str
    new_version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    diff: RegulationDiff = Field(default_factory=lambda: RegulationDiff(old_version="", new_version=""))
    total_changes: int = 0
    substantive_changes: int = 0
    impacted_requirements: int = 0
    impacted_rules: int = 0
    migration_actions: list[str] = Field(default_factory=list)
