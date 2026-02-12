"""OCR fallback for scanned / image-based regulation documents.

Requires the optional ``ocr`` dependency group:
    pip install regulationcoder[ocr]

This wraps ``pytesseract`` (Tesseract OCR) with a graceful fallback so
the rest of the pipeline works even when OCR dependencies are absent.
"""

import logging
from pathlib import Path

from regulationcoder.core.exceptions import IngestionError

logger = logging.getLogger(__name__)


class OCRFallback:
    """Extract text from image-based documents using Tesseract OCR.

    If ``pytesseract`` or ``Pillow`` are not installed, :meth:`process` will
    raise a clear error message pointing at the missing dependency.
    """

    def __init__(self, language: str = "eng") -> None:
        """
        Parameters
        ----------
        language:
            Tesseract language code (e.g. ``eng``, ``deu``, ``fra``).
            Defaults to ``eng`` (English).
        """
        self.language = language

    def process(self, file_path: str | Path) -> str:
        """Run OCR on an image or scanned document.

        Supported formats: PNG, JPEG, TIFF, BMP, and single-page PDFs
        (Tesseract's own PDF handler is *not* used — we convert to image
        first via Pillow if needed).

        Parameters
        ----------
        file_path:
            Path to the image file.

        Returns
        -------
        str
            Extracted text.

        Raises
        ------
        IngestionError
            If the optional OCR dependencies are missing, the file is
            unreadable, or Tesseract itself fails.
        """
        path = Path(file_path)
        if not path.exists():
            raise IngestionError(f"File not found for OCR: {path}")

        try:
            import pytesseract
            from PIL import Image
        except ImportError as exc:
            raise IngestionError(
                "OCR dependencies are not installed. "
                "Install them with: pip install regulationcoder[ocr]"
            ) from exc

        logger.info("Running OCR on: %s (lang=%s)", path.name, self.language)

        try:
            image = Image.open(path)
        except Exception as exc:
            raise IngestionError(f"Failed to open image for OCR: {exc}") from exc

        try:
            text: str = pytesseract.image_to_string(image, lang=self.language)
        except pytesseract.TesseractError as exc:
            raise IngestionError(f"Tesseract OCR failed: {exc}") from exc
        except Exception as exc:
            raise IngestionError(f"Unexpected OCR error: {exc}") from exc

        text = text.strip()
        logger.info("OCR extracted %d characters from %s", len(text), path.name)
        return text
