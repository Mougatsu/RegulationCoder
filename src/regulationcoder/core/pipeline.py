"""PipelineOrchestrator — end-to-end pipeline from document to compliance artifacts."""

import logging

from regulationcoder.audit.logger import AuditLogger
from regulationcoder.core.config import Settings, get_settings
from regulationcoder.core.judge import GateA, GateB, GateC
from regulationcoder.models.audit_entry import AuditAction
from regulationcoder.models.clause import Clause
from regulationcoder.models.judge_report import JudgeReport, Verdict
from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Orchestrates the full regulation-to-code pipeline with judge gating.

    Stages:
    1. Ingestion — PDF/HTML → raw text
    2. Parsing — raw text → Clause objects
    3. Extraction — Clauses → Requirements (+ Gate A)
    4. Formalization — Requirements → Rules (+ Gate B)
    5. Code Generation — Rules → Python evaluation functions (+ Gate C)
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.audit = AuditLogger(self.settings.audit_log_dir)
        self.gate_a = GateA(self.settings)
        self.gate_b = GateB(self.settings)
        self.gate_c = GateC(self.settings)

    def run_ingestion(self, file_path: str) -> str:
        """Stage 1: Ingest a regulation document and return raw text."""
        from regulationcoder.ingestion.pdf_processor import PDFProcessor
        from regulationcoder.ingestion.html_scraper import HTMLScraper
        from regulationcoder.ingestion.normalizer import DocumentNormalizer

        if file_path.lower().endswith(".pdf"):
            processor = PDFProcessor(self.settings)
            raw = processor.process(file_path)
        elif file_path.lower().endswith((".html", ".htm")):
            scraper = HTMLScraper()
            raw = scraper.scrape_file(file_path)
        else:
            with open(file_path, encoding="utf-8") as f:
                raw = f.read()

        normalizer = DocumentNormalizer()
        text = normalizer.normalize(raw)

        self.audit.log(
            action=AuditAction.INGEST,
            stage="ingestion",
            target_ids=[file_path],
            details={"file": file_path, "length": len(text)},
        )

        logger.info("Ingested %d characters from %s", len(text), file_path)
        return text

    def run_parsing(
        self, text: str, regulation_id: str, document_version: str
    ) -> list[Clause]:
        """Stage 2: Parse raw text into Clause objects."""
        from regulationcoder.parser.segmenter import ClauseSegmenter

        segmenter = ClauseSegmenter()
        clauses = segmenter.segment(text, regulation_id, document_version)

        self.audit.log(
            action=AuditAction.PARSE,
            stage="parsing",
            target_ids=[c.id for c in clauses],
            details={"clause_count": len(clauses)},
        )

        logger.info("Parsed %d clauses", len(clauses))
        return clauses

    def run_extraction(
        self, clauses: list[Clause]
    ) -> tuple[list[Requirement], list[JudgeReport]]:
        """Stage 3: Extract requirements from clauses, with Gate A validation."""
        from regulationcoder.extraction.requirement_extractor import (
            RequirementExtractor,
        )

        extractor = RequirementExtractor(self.settings)
        all_requirements: list[Requirement] = []
        all_reports: list[JudgeReport] = []

        for clause in clauses:
            requirements = extractor.extract(clause)

            for req in requirements:
                # Gate A validation
                parent_context = f"Article {clause.article_number}"
                report = self.gate_a.evaluate(
                    clause_id=clause.id,
                    clause_text=clause.text,
                    article_ref=f"Article {clause.article_number}",
                    parent_context=parent_context,
                    requirement_json=req.model_dump_json(indent=2),
                )
                all_reports.append(report)

                if report.verdict == Verdict.APPROVE:
                    all_requirements.append(req)
                    logger.info("Gate A APPROVED: %s", req.id)
                elif report.verdict == Verdict.REVISE:
                    logger.warning("Gate A REVISE: %s — %s", req.id, report.findings)
                    # Accept with warnings for now
                    all_requirements.append(req)
                else:
                    logger.error("Gate A BLOCKED: %s — %s", req.id, report.findings)

        self.audit.log(
            action=AuditAction.EXTRACT,
            stage="extraction",
            target_ids=[r.id for r in all_requirements],
            details={
                "requirement_count": len(all_requirements),
                "blocked_count": sum(
                    1 for r in all_reports if r.verdict == Verdict.BLOCK
                ),
            },
        )

        return all_requirements, all_reports

    def run_formalization(
        self, requirements: list[Requirement]
    ) -> tuple[list[Rule], list[JudgeReport]]:
        """Stage 4: Formalize requirements into rules, with Gate B validation."""
        from regulationcoder.formalization.rule_generator import RuleGenerator

        generator = RuleGenerator(self.settings)
        all_rules: list[Rule] = []
        all_reports: list[JudgeReport] = []

        for req in requirements:
            rule = generator.generate(req)

            # Gate B validation
            report = self.gate_b.evaluate(
                requirement_json=req.model_dump_json(indent=2),
                rule_json=rule.model_dump_json(indent=2),
            )
            all_reports.append(report)

            if report.verdict in (Verdict.APPROVE, Verdict.REVISE):
                all_rules.append(rule)
                logger.info("Gate B %s: %s", report.verdict.value, rule.id)
            else:
                logger.error("Gate B BLOCKED: %s — %s", rule.id, report.findings)

        self.audit.log(
            action=AuditAction.FORMALIZE,
            stage="formalization",
            target_ids=[r.id for r in all_rules],
            details={"rule_count": len(all_rules)},
        )

        return all_rules, all_reports

    def run_codegen(
        self, rules: list[Rule]
    ) -> tuple[dict[str, str], dict[str, str], list[JudgeReport]]:
        """Stage 5: Generate Python evaluation code, with Gate C validation.

        Returns (code_files, test_files, judge_reports).
        """
        from regulationcoder.codegen.sdk_generator import SDKGenerator
        from regulationcoder.codegen.test_generator import TestGenerator

        sdk_gen = SDKGenerator(self.settings)
        test_gen = TestGenerator()
        code_files: dict[str, str] = {}
        test_files: dict[str, str] = {}
        all_reports: list[JudgeReport] = []

        for rule in rules:
            code = sdk_gen.generate(rule)
            tests = test_gen.generate(rule)

            # Gate C validation
            report = self.gate_c.evaluate(
                rule_json=rule.model_dump_json(indent=2),
                generated_code=code,
                test_code=tests,
            )
            all_reports.append(report)

            if report.verdict in (Verdict.APPROVE, Verdict.REVISE):
                code_files[rule.id] = code
                test_files[rule.id] = tests
                logger.info("Gate C %s: %s", report.verdict.value, rule.id)
            else:
                logger.error("Gate C BLOCKED: %s — %s", rule.id, report.findings)

        self.audit.log(
            action=AuditAction.CODEGEN,
            stage="codegen",
            target_ids=list(code_files.keys()),
            details={"generated_count": len(code_files)},
        )

        return code_files, test_files, all_reports

    def run_full_pipeline(
        self, file_path: str, regulation_id: str, document_version: str
    ) -> dict:
        """Run the complete pipeline from document to artifacts."""
        logger.info("Starting full pipeline for %s", file_path)

        text = self.run_ingestion(file_path)
        clauses = self.run_parsing(text, regulation_id, document_version)
        requirements, gate_a_reports = self.run_extraction(clauses)
        rules, gate_b_reports = self.run_formalization(requirements)
        code_files, test_files, gate_c_reports = self.run_codegen(rules)

        return {
            "clauses": clauses,
            "requirements": requirements,
            "rules": rules,
            "code_files": code_files,
            "test_files": test_files,
            "gate_a_reports": gate_a_reports,
            "gate_b_reports": gate_b_reports,
            "gate_c_reports": gate_c_reports,
        }
