"""SQLAlchemy ORM models for persistent storage."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RegulationDB(Base):
    __tablename__ = "regulations"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)
    document_version: Mapped[str] = mapped_column(String(100), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(100), default="European Union")
    language: Mapped[str] = mapped_column(String(10), default="en")
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_file: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    total_articles: Mapped[int] = mapped_column(Integer, default=0)
    total_clauses: Mapped[int] = mapped_column(Integer, default=0)


class ClauseDB(Base):
    __tablename__ = "clauses"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    regulation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    document_version: Mapped[str] = mapped_column(String(100), nullable=False)
    article_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    paragraph_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    subsection_letter: Mapped[str | None] = mapped_column(String(10), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en")
    page_ref: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parent_clause_id: Mapped[str | None] = mapped_column(String(255), nullable=True)


class RequirementDB(Base):
    __tablename__ = "requirements"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    clause_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    modality: Mapped[str] = mapped_column(String(20), nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    object: Mapped[str] = mapped_column(Text, nullable=False)
    conditions: Mapped[dict] = mapped_column(JSONB, default=list)
    exceptions: Mapped[dict] = mapped_column(JSONB, default=list)
    scope: Mapped[str] = mapped_column(Text, default="")
    jurisdiction: Mapped[str] = mapped_column(String(100), default="European Union")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    ambiguity_notes: Mapped[str] = mapped_column(Text, default="")
    citations: Mapped[dict] = mapped_column(JSONB, default=list)


class RuleDB(Base):
    __tablename__ = "rules"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    requirement_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    rule_type: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    inputs_needed: Mapped[dict] = mapped_column(JSONB, default=list)
    evaluation_logic: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="medium")
    remediation: Mapped[str] = mapped_column(Text, default="")
    test_cases: Mapped[dict] = mapped_column(JSONB, default=list)
    citations: Mapped[dict] = mapped_column(JSONB, default=list)


class JudgeReportDB(Base):
    __tablename__ = "judge_reports"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    stage: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    target_ids: Mapped[dict] = mapped_column(JSONB, default=list)
    verdict: Mapped[str] = mapped_column(String(20), nullable=False)
    scores: Mapped[dict] = mapped_column(JSONB, default=dict)
    findings: Mapped[dict] = mapped_column(JSONB, default=list)
    required_fixes: Mapped[dict] = mapped_column(JSONB, default=list)
    citations_checked: Mapped[dict] = mapped_column(JSONB, default=list)
    model_used: Mapped[str] = mapped_column(String(100), default="")
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ComplianceReportDB(Base):
    __tablename__ = "compliance_reports"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    regulation_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    regulation_version: Mapped[str] = mapped_column(String(100), default="")
    system_name: Mapped[str] = mapped_column(Text, nullable=False)
    provider_name: Mapped[str] = mapped_column(Text, nullable=False)
    evaluation_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    summary: Mapped[dict] = mapped_column(JSONB, default=dict)
    rule_results: Mapped[dict] = mapped_column(JSONB, default=list)
    critical_gaps: Mapped[dict] = mapped_column(JSONB, default=list)
    high_gaps: Mapped[dict] = mapped_column(JSONB, default=list)
    medium_gaps: Mapped[dict] = mapped_column(JSONB, default=list)
    overall_verdict: Mapped[str] = mapped_column(String(30), default="non_compliant")


class AuditEntryDB(Base):
    __tablename__ = "audit_entries"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    action: Mapped[str] = mapped_column(String(30), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    actor: Mapped[str] = mapped_column(String(100), default="system")
    target_ids: Mapped[dict] = mapped_column(JSONB, default=list)
    input_hash: Mapped[str] = mapped_column(String(64), default="")
    output_hash: Mapped[str] = mapped_column(String(64), default="")
    previous_hash: Mapped[str] = mapped_column(String(64), default="")
    entry_hash: Mapped[str] = mapped_column(String(64), default="")
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    model_used: Mapped[str] = mapped_column(String(100), default="")
    verdict: Mapped[str] = mapped_column(String(20), default="")
