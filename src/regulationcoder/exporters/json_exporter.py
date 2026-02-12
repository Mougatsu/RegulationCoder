"""JSON exporter for ComplianceReport."""

import json
import logging
import os

from regulationcoder.models.evaluation import ComplianceReport

logger = logging.getLogger(__name__)


def export_report_json(report: ComplianceReport, path: str) -> None:
    """Export a ComplianceReport as a formatted JSON file.

    Parameters
    ----------
    report:
        The compliance report to export.
    path:
        Destination file path. Parent directories are created if needed.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    data = report.model_dump(mode="json")

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False, default=str)

    logger.info("Compliance report exported to JSON: %s", path)
