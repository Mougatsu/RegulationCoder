"""Language detection for ingested regulation text."""

import logging

from langdetect import DetectorFactory, LangDetectException, detect

from regulationcoder.core.exceptions import IngestionError

logger = logging.getLogger(__name__)

# Make langdetect deterministic — without this, results can vary across runs.
DetectorFactory.seed = 0


class LanguageDetector:
    """Detect the language of a text snippet.

    Uses the ``langdetect`` library which is a port of Google's
    language-detection library.  Returns ISO 639-1 two-letter codes
    (e.g. ``en``, ``de``, ``fr``).
    """

    # Minimum number of characters for reliable detection.
    MIN_TEXT_LENGTH = 20

    def detect(self, text: str) -> str:
        """Return the ISO 639-1 language code for *text*.

        Parameters
        ----------
        text:
            Body of text to analyse.  At least ~20 characters are
            recommended for reliable detection.

        Returns
        -------
        str
            Two-letter ISO 639-1 code, e.g. ``"en"``, ``"de"``, ``"fr"``.

        Raises
        ------
        IngestionError
            If the text is empty or detection fails.
        """
        if not text or not text.strip():
            raise IngestionError("Cannot detect language of empty text")

        cleaned = text.strip()
        if len(cleaned) < self.MIN_TEXT_LENGTH:
            logger.warning(
                "Text is very short (%d chars); language detection may be unreliable",
                len(cleaned),
            )

        try:
            language_code: str = detect(cleaned)
        except LangDetectException as exc:
            raise IngestionError(f"Language detection failed: {exc}") from exc

        logger.info("Detected language: %s (from %d chars)", language_code, len(cleaned))
        return language_code
