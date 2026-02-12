#!/usr/bin/env python3
"""Run the RegulationCoder demo pipeline against the TalentScreen AI profile.

This script:
1. Loads the TalentScreen AI profile from the test fixtures
2. Creates a ComplianceEngine configured for the EU AI Act
3. Runs the full evaluation
4. Prints a rich summary to the console
5. Exports JSON and HTML reports
"""

import json
import os
import sys

# Ensure the src directory is on the path when running as a script
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

from regulationcoder.core.engine import ComplianceEngine
from regulationcoder.models.profile import SystemProfile


# ---------------------------------------------------------------------------
# Colour helpers (ANSI escape codes for terminal output)
# ---------------------------------------------------------------------------
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_RESET = "\033[0m"


def _severity_colour(severity: str) -> str:
    return {
        "critical": _RED + _BOLD,
        "high": _RED,
        "medium": _YELLOW,
        "low": _DIM,
        "info": _DIM,
    }.get(severity, "")


def _verdict_colour(verdict: str) -> str:
    return {
        "pass": _GREEN,
        "fail": _RED,
        "not_applicable": _DIM,
        "manual_review": _YELLOW,
    }.get(verdict, "")


def main() -> None:
    # ----- Step 1: Load profile -----
    fixture_path = os.path.join(
        _PROJECT_ROOT, "tests", "fixtures", "talentscreen_profile.json"
    )

    if not os.path.exists(fixture_path):
        print(f"Fixture not found: {fixture_path}")
        print("Run  python scripts/generate_demo_profile.py  first.")
        sys.exit(1)

    with open(fixture_path, encoding="utf-8") as fh:
        profile_data = json.load(fh)

    profile = SystemProfile(**profile_data)
    print(f"\n{_BOLD}{'=' * 72}{_RESET}")
    print(f"{_BOLD}  RegulationCoder  --  Demo Pipeline{_RESET}")
    print(f"{_BOLD}{'=' * 72}{_RESET}")
    print(f"\n  System:     {_CYAN}{profile.system_name}{_RESET}")
    print(f"  Provider:   {profile.provider_name} ({profile.provider_jurisdiction})")
    print(f"  Version:    {profile.system_version}")
    print(f"  High-risk:  {profile.is_high_risk}")
    print(f"  Category:   {profile.high_risk_category}")
    print(f"  Annex III:  {profile.annex_iii_section}")

    # ----- Step 2: Create engine -----
    print(f"\n{_DIM}Loading EU AI Act regulation data ...{_RESET}")
    engine = ComplianceEngine(regulation="eu-ai-act-v1")

    # ----- Step 3: Evaluate -----
    print(f"{_DIM}Evaluating {profile.system_name} against {engine.regulation} ...{_RESET}\n")
    report = engine.evaluate(profile)

    # ----- Step 4: Print summary -----
    s = report.summary
    score_colour = _GREEN if s.compliance_score >= 90 else (_YELLOW if s.compliance_score >= 60 else _RED)

    print(f"{_BOLD}{'=' * 72}{_RESET}")
    print(f"{_BOLD}  EVALUATION RESULTS{_RESET}")
    print(f"{_BOLD}{'=' * 72}{_RESET}")
    print(
        f"\n  Compliance Score:   {score_colour}{_BOLD}{s.compliance_score} / 100{_RESET}"
    )
    verdict_label = report.overall_verdict.replace("_", " ").title()
    print(
        f"  Overall Verdict:    {score_colour}{_BOLD}{verdict_label}{_RESET}"
    )
    print()
    print(f"  Total Rules:        {s.total_rules}")
    print(f"  {_GREEN}Passed:{_RESET}             {s.passed}")
    print(f"  {_RED}Failed:{_RESET}             {s.failed}")
    print(f"  {_DIM}Not Applicable:{_RESET}     {s.not_applicable}")
    print(f"  {_YELLOW}Manual Review:{_RESET}      {s.manual_review}")

    # Gaps summary
    total_gaps = len(report.critical_gaps) + len(report.high_gaps) + len(report.medium_gaps)
    if total_gaps > 0:
        print(f"\n{_BOLD}{'=' * 72}{_RESET}")
        print(f"{_BOLD}  COMPLIANCE GAPS ({total_gaps} total){_RESET}")
        print(f"{_BOLD}{'=' * 72}{_RESET}\n")

        if report.critical_gaps:
            print(f"  {_RED}{_BOLD}CRITICAL ({len(report.critical_gaps)}){_RESET}")
            for g in report.critical_gaps:
                print(f"    {_RED}* {g.description}{_RESET}")
                print(f"      Rule: {g.rule_id}  |  {g.article_ref}")
                print(f"      Remediation: {g.remediation}\n")

        if report.high_gaps:
            print(f"  {_RED}HIGH ({len(report.high_gaps)}){_RESET}")
            for g in report.high_gaps:
                print(f"    {_RED}* {g.description}{_RESET}")
                print(f"      Rule: {g.rule_id}  |  {g.article_ref}")
                print(f"      Remediation: {g.remediation}\n")

        if report.medium_gaps:
            print(f"  {_YELLOW}MEDIUM ({len(report.medium_gaps)}){_RESET}")
            for g in report.medium_gaps:
                print(f"    {_YELLOW}* {g.description}{_RESET}")
                print(f"      Rule: {g.rule_id}  |  {g.article_ref}")
                print(f"      Remediation: {g.remediation}\n")

    # Per-rule details
    print(f"\n{_BOLD}{'=' * 72}{_RESET}")
    print(f"{_BOLD}  RULE-BY-RULE RESULTS{_RESET}")
    print(f"{_BOLD}{'=' * 72}{_RESET}\n")

    for r in report.rule_results:
        v_col = _verdict_colour(r.verdict.value)
        s_col = _severity_colour(r.severity)
        verdict_tag = r.verdict.value.upper().replace("_", " ")
        print(
            f"  [{v_col}{verdict_tag:>14}{_RESET}]  "
            f"[{s_col}{r.severity:>8}{_RESET}]  "
            f"{r.rule_id}  {r.title}"
        )

    # ----- Step 5: Export reports -----
    output_dir = os.path.join(_PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, "talentscreen_report.json")
    html_path = os.path.join(output_dir, "talentscreen_report.html")

    report.export_json(json_path)
    report.export_html(html_path)

    print(f"\n{_BOLD}{'=' * 72}{_RESET}")
    print(f"{_BOLD}  EXPORTS{_RESET}")
    print(f"{_BOLD}{'=' * 72}{_RESET}")
    print(f"\n  JSON report:  {json_path}")
    print(f"  HTML report:  {html_path}")
    print()
    print(
        f"{_DIM}DISCLAIMER: This report is an engineering interpretation of regulatory "
        f"requirements. It does not constitute legal advice.{_RESET}\n"
    )


if __name__ == "__main__":
    main()
