"""PDF exporter for ComplianceReport — wraps the HTML exporter + WeasyPrint."""

import logging
import os
import tempfile

from regulationcoder.models.evaluation import ComplianceReport

logger = logging.getLogger(__name__)


def export_report_pdf(report: ComplianceReport, path: str) -> None:
    """Export a ComplianceReport as a PDF file.

    The report is first rendered to HTML via
    :func:`~regulationcoder.exporters.html_exporter.export_report_html` and
    then converted to PDF using `WeasyPrint <https://weasyprint.org/>`_.

    If WeasyPrint is not installed the function raises an
    :class:`ImportError` with a helpful message.

    Parameters
    ----------
    report:
        The compliance report to export.
    path:
        Destination PDF file path. Parent directories are created if needed.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    # Import the HTML exporter to generate intermediate HTML
    from regulationcoder.exporters.html_exporter import export_report_html

    # Generate HTML to a temporary file
    tmp_fd, tmp_html_path = tempfile.mkstemp(suffix=".html", prefix="rc_report_")
    os.close(tmp_fd)

    try:
        export_report_html(report, tmp_html_path)

        try:
            from weasyprint import HTML  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "WeasyPrint is required for PDF export but is not installed. "
                "Install it with:  pip install weasyprint"
            ) from None

        HTML(filename=tmp_html_path).write_pdf(path)
        logger.info("Compliance report exported to PDF: %s", path)
    finally:
        # Clean up the temporary HTML file
        try:
            os.unlink(tmp_html_path)
        except OSError:
            pass
