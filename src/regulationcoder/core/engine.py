"""ComplianceEngine — main entry point for evaluating system profiles against regulations."""

import json
import logging
from datetime import datetime, timezone

from regulationcoder.core.config import Settings, get_settings
from regulationcoder.models.clause import Clause
from regulationcoder.models.evaluation import (
    ComplianceGap,
    ComplianceReport,
    EvaluationResult,
    RuleResult,
    RuleVerdict,
)
from regulationcoder.models.profile import SystemProfile
from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)


class ComplianceEngine:
    """Evaluate an AI system profile against a set of compliance rules.

    Usage:
        engine = ComplianceEngine(anthropic_api_key="sk-ant-...", regulation="eu-ai-act-v1")
        report = engine.evaluate(profile)
    """

    def __init__(
        self,
        anthropic_api_key: str | None = None,
        regulation: str = "eu-ai-act-v1",
        settings: Settings | None = None,
    ):
        self.settings = settings or get_settings()
        if anthropic_api_key:
            self.settings.anthropic_api_key = anthropic_api_key
        self.regulation = regulation
        self._clauses: list[Clause] = []
        self._requirements: list[Requirement] = []
        self._rules: list[Rule] = []
        self._load_regulation()

    def _load_regulation(self) -> None:
        """Load pre-built regulation data (clauses, requirements, rules)."""
        if self.regulation == "eu-ai-act-v1":
            from regulationcoder.rules.eu_ai_act_v1 import (
                get_clauses,
                get_requirements,
                get_rules,
            )

            self._clauses = get_clauses()
            self._requirements = get_requirements()
            self._rules = get_rules()
            logger.info(
                "Loaded %d clauses, %d requirements, %d rules for %s",
                len(self._clauses),
                len(self._requirements),
                len(self._rules),
                self.regulation,
            )

    def evaluate(self, profile: SystemProfile) -> ComplianceReport:
        """Evaluate a system profile against all loaded rules.

        Returns a ComplianceReport with per-rule results, gaps, and overall score.
        """
        rule_results: list[RuleResult] = []
        critical_gaps: list[ComplianceGap] = []
        high_gaps: list[ComplianceGap] = []
        medium_gaps: list[ComplianceGap] = []

        profile_dict = profile.model_dump()

        for rule in self._rules:
            result = self._evaluate_rule(rule, profile_dict)
            rule_results.append(result)

            if result.verdict == RuleVerdict.FAIL:
                gap = ComplianceGap(
                    rule_id=rule.id,
                    requirement_id=rule.requirement_id,
                    description=result.details or rule.title,
                    severity=rule.severity.value,
                    remediation=rule.remediation,
                    article_ref=result.article_ref,
                    citations=rule.citations,
                )
                if rule.severity.value == "critical":
                    critical_gaps.append(gap)
                elif rule.severity.value == "high":
                    high_gaps.append(gap)
                else:
                    medium_gaps.append(gap)

        passed = sum(1 for r in rule_results if r.verdict == RuleVerdict.PASS)
        failed = sum(1 for r in rule_results if r.verdict == RuleVerdict.FAIL)
        na = sum(1 for r in rule_results if r.verdict == RuleVerdict.NOT_APPLICABLE)
        manual = sum(1 for r in rule_results if r.verdict == RuleVerdict.MANUAL_REVIEW)
        applicable = passed + failed
        score = round((passed / applicable * 100) if applicable > 0 else 0, 1)

        if score >= 90 and not critical_gaps:
            overall = "compliant"
        elif score >= 60:
            overall = "partial_compliance"
        else:
            overall = "non_compliant"

        now = datetime.now(timezone.utc)
        report = ComplianceReport(
            id=f"RPT-{self.regulation}-{now.strftime('%Y%m%d%H%M%S')}",
            regulation_id=self.regulation,
            system_name=profile.system_name,
            provider_name=profile.provider_name,
            evaluation_date=now,
            summary=EvaluationResult(
                total_rules=len(rule_results),
                passed=passed,
                failed=failed,
                not_applicable=na,
                manual_review=manual,
                compliance_score=score,
            ),
            rule_results=rule_results,
            critical_gaps=critical_gaps,
            high_gaps=high_gaps,
            medium_gaps=medium_gaps,
            overall_verdict=overall,
        )

        logger.info(
            "Evaluation complete: %s — score %s/100, %d critical gaps",
            overall,
            score,
            len(critical_gaps),
        )
        return report

    def _evaluate_rule(self, rule: Rule, profile_dict: dict) -> RuleResult:
        """Evaluate a single rule against the profile data."""
        article_ref = ""
        if rule.citations:
            article_ref = rule.citations[0].article_ref

        # Check if the rule is manual-only
        if rule.rule_type.value == "manual":
            return RuleResult(
                rule_id=rule.id,
                requirement_id=rule.requirement_id,
                title=rule.title,
                verdict=RuleVerdict.MANUAL_REVIEW,
                severity=rule.severity.value,
                details="Requires manual assessment",
                article_ref=article_ref,
                citations=rule.citations,
            )

        # Execute rule evaluation logic
        try:
            verdict = self._execute_evaluation(rule, profile_dict)
        except Exception as e:
            logger.warning("Error evaluating rule %s: %s", rule.id, e)
            verdict = "manual_review"

        verdict_map = {
            "pass": RuleVerdict.PASS,
            "fail": RuleVerdict.FAIL,
            "not_applicable": RuleVerdict.NOT_APPLICABLE,
            "manual_review": RuleVerdict.MANUAL_REVIEW,
        }

        return RuleResult(
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            title=rule.title,
            verdict=verdict_map.get(verdict, RuleVerdict.MANUAL_REVIEW),
            severity=rule.severity.value,
            details=rule.description,
            remediation=rule.remediation,
            article_ref=article_ref,
            citations=rule.citations,
        )

    def _execute_evaluation(self, rule: Rule, profile_dict: dict) -> str:
        """Execute evaluation logic from a rule against profile data.

        Uses a safe evaluation approach — resolves dotted field paths from the
        profile dictionary and applies the rule's evaluation logic.
        """
        # Resolve inputs from profile
        inputs = {}
        for field_path in rule.inputs_needed:
            value = self._resolve_field(profile_dict, field_path)
            # Create a simple variable name from the last segment
            var_name = field_path.split(".")[-1]
            inputs[var_name] = value

        # Execute using the generated evaluation function if available
        try:
            from regulationcoder.rules.eu_ai_act_v1 import get_evaluation_function

            eval_fn = get_evaluation_function(rule.id)
            if eval_fn:
                return eval_fn(profile_dict)
        except (ImportError, AttributeError):
            pass

        # Fallback: interpret evaluation_logic as simple Python
        try:
            local_vars = {**inputs, "result": "manual_review"}
            exec(rule.evaluation_logic, {"__builtins__": {}}, local_vars)  # noqa: S102
            return local_vars.get("result", "manual_review")
        except Exception:
            return "manual_review"

    @staticmethod
    def _resolve_field(data: dict, field_path: str):
        """Resolve a dotted field path like 'system_profile.bias_report.covers_health'."""
        # Strip 'system_profile.' prefix if present
        if field_path.startswith("system_profile."):
            field_path = field_path[len("system_profile."):]

        parts = field_path.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
            if current is None:
                return None
        return current
