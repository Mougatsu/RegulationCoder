"""HTML exporter for ComplianceReport using Jinja2."""

import logging
import os

from jinja2 import Environment, BaseLoader

from regulationcoder.models.evaluation import ComplianceReport

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Embedded Jinja2 HTML template
# ---------------------------------------------------------------------------
_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Compliance Report — {{ report.system_name }}</title>
<style>
  /* ---------- Reset & base ---------- */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background: #f8fafc;
    line-height: 1.6;
    padding: 0;
  }

  /* ---------- Page wrapper ---------- */
  .page { max-width: 960px; margin: 0 auto; padding: 40px 32px; }

  /* ---------- Header ---------- */
  .header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
    color: #fff;
    padding: 36px 40px;
    border-radius: 12px;
    margin-bottom: 32px;
  }
  .header h1 { font-size: 1.75rem; font-weight: 700; margin-bottom: 4px; }
  .header .subtitle { opacity: 0.85; font-size: 0.95rem; }
  .header .meta { margin-top: 16px; display: flex; flex-wrap: wrap; gap: 24px; font-size: 0.9rem; }
  .header .meta span { opacity: 0.9; }

  /* ---------- Scorecard ---------- */
  .scorecard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }
  .score-box {
    background: #fff;
    border-radius: 10px;
    padding: 20px 16px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .score-box .value { font-size: 2rem; font-weight: 700; }
  .score-box .label { font-size: 0.82rem; color: #64748b; margin-top: 4px; }
  .score-box.pass .value { color: #16a34a; }
  .score-box.fail .value { color: #dc2626; }
  .score-box.na .value   { color: #6b7280; }
  .score-box.manual .value { color: #d97706; }
  .score-box.total .value  { color: #2563eb; }

  /* ---------- Verdict badge ---------- */
  .verdict-banner {
    padding: 14px 24px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 32px;
    text-align: center;
  }
  .verdict-compliant     { background: #dcfce7; color: #15803d; }
  .verdict-partial       { background: #fef9c3; color: #a16207; }
  .verdict-non_compliant { background: #fee2e2; color: #b91c1c; }

  /* ---------- Section ---------- */
  .section { margin-bottom: 36px; }
  .section h2 {
    font-size: 1.2rem; font-weight: 600;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 16px;
    color: #1e3a5f;
  }

  /* ---------- Table ---------- */
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
  th { background: #f1f5f9; font-weight: 600; color: #475569; }
  tr:hover td { background: #f8fafc; }

  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
  }
  .badge-pass   { background: #dcfce7; color: #15803d; }
  .badge-fail   { background: #fee2e2; color: #b91c1c; }
  .badge-na     { background: #f3f4f6; color: #6b7280; }
  .badge-manual { background: #fef3c7; color: #92400e; }

  .severity-critical { color: #b91c1c; font-weight: 700; }
  .severity-high     { color: #dc2626; }
  .severity-medium   { color: #d97706; }
  .severity-low      { color: #6b7280; }

  /* ---------- Gap card ---------- */
  .gap-card {
    background: #fff;
    border-left: 4px solid #dc2626;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .gap-card.high { border-left-color: #f97316; }
  .gap-card.medium { border-left-color: #eab308; }
  .gap-card .gap-title { font-weight: 600; margin-bottom: 4px; }
  .gap-card .gap-meta { font-size: 0.82rem; color: #64748b; margin-bottom: 6px; }
  .gap-card .gap-remediation { font-size: 0.88rem; color: #334155; }

  /* ---------- Disclaimer ---------- */
  .disclaimer {
    margin-top: 40px;
    padding: 20px 24px;
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    font-size: 0.84rem;
    color: #92400e;
    line-height: 1.7;
  }

  /* ---------- Footer ---------- */
  .footer {
    text-align: center;
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #e2e8f0;
  }
</style>
</head>
<body>
<div class="page">

  <!-- Header -->
  <div class="header">
    <h1>Compliance Report</h1>
    <div class="subtitle">{{ report.regulation_id }}{% if report.regulation_version %} &mdash; {{ report.regulation_version }}{% endif %}</div>
    <div class="meta">
      <span><strong>System:</strong> {{ report.system_name }}</span>
      <span><strong>Provider:</strong> {{ report.provider_name }}</span>
      <span><strong>Date:</strong> {{ report.evaluation_date.strftime('%Y-%m-%d %H:%M UTC') }}</span>
      <span><strong>Report ID:</strong> {{ report.id }}</span>
    </div>
  </div>

  <!-- Verdict -->
  {% set verdict_class = 'verdict-compliant' if report.overall_verdict == 'compliant' else ('verdict-partial' if report.overall_verdict == 'partial_compliance' else 'verdict-non_compliant') %}
  <div class="verdict-banner {{ verdict_class }}">
    Overall Verdict: {{ report.overall_verdict | replace('_', ' ') | title }}
    &nbsp;&mdash;&nbsp; Score: {{ report.summary.compliance_score }}%
  </div>

  <!-- Scorecard -->
  <div class="scorecard">
    <div class="score-box total"><div class="value">{{ report.summary.total_rules }}</div><div class="label">Total Rules</div></div>
    <div class="score-box pass"><div class="value">{{ report.summary.passed }}</div><div class="label">Passed</div></div>
    <div class="score-box fail"><div class="value">{{ report.summary.failed }}</div><div class="label">Failed</div></div>
    <div class="score-box na"><div class="value">{{ report.summary.not_applicable }}</div><div class="label">N/A</div></div>
    <div class="score-box manual"><div class="value">{{ report.summary.manual_review }}</div><div class="label">Manual Review</div></div>
  </div>

  <!-- Rule Results Table -->
  <div class="section">
    <h2>Rule Results</h2>
    <table>
      <thead>
        <tr>
          <th>Rule ID</th>
          <th>Title</th>
          <th>Verdict</th>
          <th>Severity</th>
          <th>Article</th>
        </tr>
      </thead>
      <tbody>
      {% for r in report.rule_results %}
        <tr>
          <td><code>{{ r.rule_id }}</code></td>
          <td>{{ r.title }}</td>
          <td>
            {% if r.verdict.value == 'pass' %}
              <span class="badge badge-pass">Pass</span>
            {% elif r.verdict.value == 'fail' %}
              <span class="badge badge-fail">Fail</span>
            {% elif r.verdict.value == 'not_applicable' %}
              <span class="badge badge-na">N/A</span>
            {% else %}
              <span class="badge badge-manual">Manual</span>
            {% endif %}
          </td>
          <td><span class="severity-{{ r.severity }}">{{ r.severity | title }}</span></td>
          <td>{{ r.article_ref }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>

  <!-- Gaps -->
  {% if report.critical_gaps or report.high_gaps or report.medium_gaps %}
  <div class="section">
    <h2>Compliance Gaps</h2>

    {% for gap in report.critical_gaps %}
    <div class="gap-card critical">
      <div class="gap-title">[CRITICAL] {{ gap.description }}</div>
      <div class="gap-meta">Rule: {{ gap.rule_id }} &bull; Requirement: {{ gap.requirement_id }} &bull; {{ gap.article_ref }}</div>
      <div class="gap-remediation"><strong>Remediation:</strong> {{ gap.remediation }}</div>
    </div>
    {% endfor %}

    {% for gap in report.high_gaps %}
    <div class="gap-card high">
      <div class="gap-title">[HIGH] {{ gap.description }}</div>
      <div class="gap-meta">Rule: {{ gap.rule_id }} &bull; Requirement: {{ gap.requirement_id }} &bull; {{ gap.article_ref }}</div>
      <div class="gap-remediation"><strong>Remediation:</strong> {{ gap.remediation }}</div>
    </div>
    {% endfor %}

    {% for gap in report.medium_gaps %}
    <div class="gap-card medium">
      <div class="gap-title">[MEDIUM] {{ gap.description }}</div>
      <div class="gap-meta">Rule: {{ gap.rule_id }} &bull; Requirement: {{ gap.requirement_id }} &bull; {{ gap.article_ref }}</div>
      <div class="gap-remediation"><strong>Remediation:</strong> {{ gap.remediation }}</div>
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Disclaimer -->
  <div class="disclaimer">
    {{ report.disclaimer }}
  </div>

  <!-- Footer -->
  <div class="footer">
    Generated by RegulationCoder v0.1.0
  </div>

</div>
</body>
</html>
"""


def export_report_html(report: ComplianceReport, path: str) -> None:
    """Render a ComplianceReport as a styled HTML file.

    Parameters
    ----------
    report:
        The compliance report to export.
    path:
        Destination file path. Parent directories are created if needed.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    env = Environment(loader=BaseLoader(), autoescape=True)
    template = env.from_string(_HTML_TEMPLATE)
    html = template.render(report=report)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)

    logger.info("Compliance report exported to HTML: %s", path)
