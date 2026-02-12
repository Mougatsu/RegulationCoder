"""RegulationCoder CLI — Click-based command-line interface."""

import json
import os
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


@click.group()
def cli():
    """RegulationCoder - Converting regulations into compliance software."""


@cli.command()
@click.option(
    "--profile",
    required=True,
    type=click.Path(exists=True),
    help="Path to system profile JSON",
)
@click.option(
    "--regulation",
    default="eu-ai-act-v1",
    help="Regulation identifier",
)
@click.option(
    "--output",
    default="compliance_report.json",
    help="Output file path",
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["json", "html", "both"]),
    default="json",
    help="Output format",
)
def check(profile: str, regulation: str, output: str, fmt: str):
    """Evaluate a system profile against a regulation."""
    from regulationcoder.core.engine import ComplianceEngine
    from regulationcoder.models.profile import SystemProfile

    console.print(
        Panel(
            "[bold blue]RegulationCoder[/bold blue] - Compliance Check",
            subtitle=f"Regulation: {regulation}",
        )
    )

    # Load profile JSON
    console.print(f"[dim]Loading profile from:[/dim] {profile}")
    try:
        with open(profile, encoding="utf-8") as f:
            profile_data = json.load(f)
        system_profile = SystemProfile(**profile_data)
    except (json.JSONDecodeError, ValueError) as e:
        console.print(f"[bold red]Error loading profile:[/bold red] {e}")
        sys.exit(1)

    console.print(
        f"[dim]System:[/dim] {system_profile.system_name} "
        f"[dim]by[/dim] {system_profile.provider_name}"
    )

    # Create engine and evaluate
    console.print("[dim]Initializing compliance engine...[/dim]")
    try:
        engine = ComplianceEngine(regulation=regulation)
    except Exception as e:
        console.print(f"[bold red]Error initializing engine:[/bold red] {e}")
        sys.exit(1)

    console.print("[dim]Running evaluation...[/dim]")
    report = engine.evaluate(system_profile)

    # Export results
    base, ext = os.path.splitext(output)
    if fmt in ("json", "both"):
        json_path = output if fmt == "json" else f"{base}.json"
        report.export_json(json_path)
        console.print(f"[green]JSON report saved:[/green] {json_path}")

    if fmt in ("html", "both"):
        html_path = f"{base}.html" if fmt == "both" else output.replace(".json", ".html")
        if html_path == output and not html_path.endswith(".html"):
            html_path = f"{base}.html"
        report.export_html(html_path)
        console.print(f"[green]HTML report saved:[/green] {html_path}")

    # Print summary table
    console.print()
    _print_summary_table(report)
    _print_gaps_summary(report)

    # Overall verdict
    verdict_color = {
        "compliant": "green",
        "partial_compliance": "yellow",
        "non_compliant": "red",
    }.get(report.overall_verdict, "red")

    console.print()
    console.print(
        Panel(
            f"[bold {verdict_color}]{report.overall_verdict.replace('_', ' ').title()}[/bold {verdict_color}]"
            f"  -  Score: {report.summary.compliance_score}%",
            title="Overall Verdict",
            border_style=verdict_color,
        )
    )


def _print_summary_table(report):
    """Print the evaluation summary as a Rich table."""
    from regulationcoder.models.evaluation import ComplianceReport

    table = Table(title="Evaluation Summary", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim", width=20)
    table.add_column("Value", justify="right")

    s = report.summary
    table.add_row("Total Rules", str(s.total_rules))
    table.add_row("Passed", f"[green]{s.passed}[/green]")
    table.add_row("Failed", f"[red]{s.failed}[/red]")
    table.add_row("Not Applicable", str(s.not_applicable))
    table.add_row("Manual Review", f"[yellow]{s.manual_review}[/yellow]")
    table.add_row("Compliance Score", f"[bold]{s.compliance_score}%[/bold]")

    console.print(table)

    # Print per-rule results table
    console.print()
    rule_table = Table(
        title="Rule Results",
        show_header=True,
        header_style="bold cyan",
        show_lines=True,
    )
    rule_table.add_column("Rule ID", style="dim", no_wrap=True)
    rule_table.add_column("Title", width=40)
    rule_table.add_column("Verdict", justify="center")
    rule_table.add_column("Severity", justify="center")
    rule_table.add_column("Article", style="dim")

    verdict_styles = {
        "pass": "[green]PASS[/green]",
        "fail": "[red]FAIL[/red]",
        "not_applicable": "[dim]N/A[/dim]",
        "manual_review": "[yellow]MANUAL[/yellow]",
    }
    severity_styles = {
        "critical": "[bold red]CRITICAL[/bold red]",
        "high": "[red]HIGH[/red]",
        "medium": "[yellow]MEDIUM[/yellow]",
        "low": "[dim]LOW[/dim]",
        "info": "[dim]INFO[/dim]",
    }

    for r in report.rule_results:
        rule_table.add_row(
            r.rule_id,
            r.title,
            verdict_styles.get(r.verdict.value, r.verdict.value),
            severity_styles.get(r.severity, r.severity),
            r.article_ref,
        )

    console.print(rule_table)


def _print_gaps_summary(report):
    """Print a summary of compliance gaps."""
    total_gaps = len(report.critical_gaps) + len(report.high_gaps) + len(report.medium_gaps)
    if total_gaps == 0:
        console.print("\n[green]No compliance gaps found.[/green]")
        return

    console.print()
    gap_table = Table(
        title=f"Compliance Gaps ({total_gaps} total)",
        show_header=True,
        header_style="bold red",
        show_lines=True,
    )
    gap_table.add_column("Severity", justify="center", width=10)
    gap_table.add_column("Rule", style="dim", no_wrap=True)
    gap_table.add_column("Description", width=40)
    gap_table.add_column("Article")
    gap_table.add_column("Remediation", width=35)

    for gap in report.critical_gaps:
        gap_table.add_row(
            "[bold red]CRITICAL[/bold red]",
            gap.rule_id,
            gap.description,
            gap.article_ref,
            gap.remediation,
        )
    for gap in report.high_gaps:
        gap_table.add_row(
            "[red]HIGH[/red]",
            gap.rule_id,
            gap.description,
            gap.article_ref,
            gap.remediation,
        )
    for gap in report.medium_gaps:
        gap_table.add_row(
            "[yellow]MEDIUM[/yellow]",
            gap.rule_id,
            gap.description,
            gap.article_ref,
            gap.remediation,
        )

    console.print(gap_table)


@cli.command()
@click.option(
    "--file",
    "file_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to regulation document (PDF or HTML)",
)
@click.option("--regulation-id", required=True, help="Regulation identifier")
@click.option("--version", required=True, help="Document version identifier")
def ingest(file_path: str, regulation_id: str, version: str):
    """Ingest a regulation document (PDF/HTML)."""
    from regulationcoder.core.pipeline import PipelineOrchestrator

    console.print(
        Panel(
            "[bold blue]RegulationCoder[/bold blue] - Document Ingestion",
            subtitle=f"Regulation: {regulation_id} v{version}",
        )
    )

    console.print(f"[dim]File:[/dim] {file_path}")
    console.print(f"[dim]Regulation:[/dim] {regulation_id}")
    console.print(f"[dim]Version:[/dim] {version}")

    orchestrator = PipelineOrchestrator()

    # Stage 1: Ingestion
    console.print("\n[bold cyan][1/2][/bold cyan] Ingesting document...")
    try:
        text = orchestrator.run_ingestion(file_path)
        console.print(f"  [green]Extracted {len(text):,} characters[/green]")
    except Exception as e:
        console.print(f"  [bold red]Ingestion failed:[/bold red] {e}")
        sys.exit(1)

    # Stage 2: Parsing
    console.print("[bold cyan][2/2][/bold cyan] Parsing into clauses...")
    try:
        clauses = orchestrator.run_parsing(text, regulation_id, version)
        console.print(f"  [green]Parsed {len(clauses)} clauses[/green]")
    except Exception as e:
        console.print(f"  [bold red]Parsing failed:[/bold red] {e}")
        sys.exit(1)

    # Summary
    console.print()
    table = Table(title="Ingestion Summary", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")
    table.add_row("Source File", os.path.basename(file_path))
    table.add_row("Regulation ID", regulation_id)
    table.add_row("Version", version)
    table.add_row("Characters Extracted", f"{len(text):,}")
    table.add_row("Clauses Parsed", str(len(clauses)))

    console.print(table)
    console.print("\n[green]Ingestion complete.[/green]")


@cli.command()
@click.option("--old-version", required=True, help="Old regulation version")
@click.option("--new-version", required=True, help="New regulation version")
@click.option("--regulation-id", default="eu-ai-act", help="Regulation identifier")
@click.option("--output", default="diff_report.json", help="Output file path")
def diff(old_version: str, new_version: str, regulation_id: str, output: str):
    """Compare two regulation versions."""
    console.print(
        Panel(
            "[bold blue]RegulationCoder[/bold blue] - Version Diff",
            subtitle=f"{regulation_id}: {old_version} -> {new_version}",
        )
    )

    console.print(f"[dim]Regulation:[/dim] {regulation_id}")
    console.print(f"[dim]Old Version:[/dim] {old_version}")
    console.print(f"[dim]New Version:[/dim] {new_version}")

    # For the MVP, create a placeholder diff report
    from regulationcoder.models.diff import DiffReport, RegulationDiff

    diff_result = DiffReport(
        id=f"DIFF-{regulation_id}-{old_version}-{new_version}",
        regulation_id=regulation_id,
        old_version=old_version,
        new_version=new_version,
        diff=RegulationDiff(
            old_version=old_version,
            new_version=new_version,
            clause_changes=[],
            impacted_items=[],
        ),
        total_changes=0,
        substantive_changes=0,
        impacted_requirements=0,
        impacted_rules=0,
        migration_actions=[],
    )

    # Export
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(diff_result.model_dump(mode="json"), f, indent=2, default=str)

    console.print(f"\n[green]Diff report saved:[/green] {output}")

    # Summary
    table = Table(title="Diff Summary", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")
    table.add_row("Total Changes", str(diff_result.total_changes))
    table.add_row("Substantive Changes", str(diff_result.substantive_changes))
    table.add_row("Impacted Requirements", str(diff_result.impacted_requirements))
    table.add_row("Impacted Rules", str(diff_result.impacted_rules))
    table.add_row("Migration Actions", str(len(diff_result.migration_actions)))

    console.print(table)


@cli.command()
@click.option(
    "--log-dir",
    default="./audit_logs",
    help="Directory containing audit log files",
)
def verify_audit(log_dir: str):
    """Verify audit log hash chain integrity."""
    from regulationcoder.audit.logger import AuditLogger

    console.print(
        Panel(
            "[bold blue]RegulationCoder[/bold blue] - Audit Verification",
            subtitle=f"Log directory: {log_dir}",
        )
    )

    log_file = os.path.join(log_dir, "audit.jsonl")
    if not os.path.exists(log_file):
        console.print(f"[yellow]No audit log found at {log_file}[/yellow]")
        return

    console.print(f"[dim]Loading audit log:[/dim] {log_file}")

    audit_logger = AuditLogger(log_dir=log_dir)
    entries = audit_logger.load_from_file(log_file)
    console.print(f"[dim]Found {len(entries)} entries[/dim]")

    if not entries:
        console.print("[yellow]No entries to verify.[/yellow]")
        return

    is_valid, errors = AuditLogger.verify_chain(entries)

    # Summary table
    table = Table(title="Audit Verification", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")
    table.add_row("Total Entries", str(len(entries)))
    table.add_row("First Entry", entries[0].timestamp.isoformat())
    table.add_row("Last Entry", entries[-1].timestamp.isoformat())
    table.add_row(
        "Chain Integrity",
        "[bold green]VALID[/bold green]" if is_valid else "[bold red]BROKEN[/bold red]",
    )

    console.print(table)

    if errors:
        console.print(f"\n[bold red]Found {len(errors)} integrity errors:[/bold red]")
        for err in errors:
            console.print(f"  [red]- {err}[/red]")
    else:
        console.print("\n[bold green]Hash chain integrity verified successfully.[/bold green]")


if __name__ == "__main__":
    cli()
