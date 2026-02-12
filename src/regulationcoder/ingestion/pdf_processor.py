"""PDF text extraction using the Anthropic API's native PDF/document support."""

import base64
import logging
from pathlib import Path

import anthropic

from regulationcoder.core.config import Settings
from regulationcoder.core.exceptions import IngestionError

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Extract text from PDF documents via the Anthropic API.

    The Anthropic Messages API supports PDF files as a first-class content type.
    We base64-encode the PDF and send it as a ``document`` content block, then
    ask the model to return the full text faithfully.
    """

    # Anthropic API imposes a 32 MB base64 limit for documents.
    MAX_PDF_SIZE_BYTES = 32 * 1024 * 1024

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        if not settings.anthropic_api_key:
            raise IngestionError("anthropic_api_key is required for PDFProcessor")
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def process(self, file_path: str | Path) -> str:
        """Extract the full text content from a PDF file.

        Parameters
        ----------
        file_path:
            Path to the PDF file on disk.

        Returns
        -------
        str
            The extracted text content of the PDF.

        Raises
        ------
        IngestionError
            If the file cannot be read or the API call fails.
        """
        path = Path(file_path)

        if not path.exists():
            raise IngestionError(f"PDF file not found: {path}")
        if not path.suffix.lower() == ".pdf":
            raise IngestionError(f"Expected a .pdf file, got: {path.suffix}")
        if path.stat().st_size > self.MAX_PDF_SIZE_BYTES:
            raise IngestionError(
                f"PDF exceeds maximum size of {self.MAX_PDF_SIZE_BYTES // (1024 * 1024)} MB"
            )

        logger.info("Processing PDF: %s (%d bytes)", path.name, path.stat().st_size)

        try:
            pdf_bytes = path.read_bytes()
        except OSError as exc:
            raise IngestionError(f"Failed to read PDF file: {exc}") from exc

        pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("ascii")

        try:
            message = self._client.messages.create(
                model=self.settings.extraction_model,
                max_tokens=16384,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": (
                                    "Extract the complete text content of this PDF document. "
                                    "Preserve the original structure including article numbers, "
                                    "paragraph numbers, subsection letters, and any numbering. "
                                    "Return only the extracted text, no commentary."
                                ),
                            },
                        ],
                    }
                ],
            )
        except anthropic.APIError as exc:
            raise IngestionError(f"Anthropic API error during PDF extraction: {exc}") from exc

        # Concatenate all text blocks in the response.
        extracted_parts: list[str] = []
        for block in message.content:
            if block.type == "text":
                extracted_parts.append(block.text)

        if not extracted_parts:
            raise IngestionError("Anthropic API returned no text content for the PDF")

        text = "\n".join(extracted_parts)
        logger.info("Extracted %d characters from %s", len(text), path.name)
        return text
