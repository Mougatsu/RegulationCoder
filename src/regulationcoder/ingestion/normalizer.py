"""Text normalisation for ingested regulation documents.

Cleans up OCR artefacts, stray headers/footers, Unicode oddities, and
whitespace irregularities that are common in official PDF exports of
EU legislation.
"""

import logging
import re
import unicodedata

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Patterns for artefacts typically left by PDF-to-text conversion
# --------------------------------------------------------------------------

# Repeated page-header/footer patterns (e.g. "Official Journal …  EN  L 123/45")
_HEADER_FOOTER_RE = re.compile(
    r"^(?:"
    r"Official Journal.*|"                      # EU OJ header lines
    r"\d{1,2}\.\d{1,2}\.\d{4}\s+EN.*|"         # Date + language code lines
    r"L\s+\d+/\d+.*|"                           # OJ L page references
    r"EN\s+EN|"                                 # Doubled language markers
    r"—\s*\d+\s*—|"                             # Em-dash page numbers
    r"\x0c"                                     # Form-feed characters
    r")$",
    re.MULTILINE,
)

# Hyphenation at line breaks introduced by PDF column wrapping:
# "regu-\nlation" → "regulation"
_HYPHEN_LINEBREAK_RE = re.compile(r"(\w)-\n(\w)")

# Multiple consecutive blank lines → single blank line
_MULTI_BLANK_RE = re.compile(r"\n{3,}")

# Unicode "smart" punctuation normalisation map
_UNICODE_REPLACEMENTS: dict[str, str] = {
    "\u2018": "'",   # left single quotation mark
    "\u2019": "'",   # right single quotation mark
    "\u201c": '"',   # left double quotation mark
    "\u201d": '"',   # right double quotation mark
    "\u2013": "-",   # en dash
    "\u2014": "-",   # em dash
    "\u2026": "...", # horizontal ellipsis
    "\u00a0": " ",   # non-breaking space
    "\u00ad": "",    # soft hyphen
    "\u200b": "",    # zero-width space
    "\u200c": "",    # zero-width non-joiner
    "\u200d": "",    # zero-width joiner
    "\ufeff": "",    # byte order mark
}


class DocumentNormalizer:
    """Clean and normalise raw text extracted from regulation documents.

    The :meth:`normalize` method applies the following transformations in
    order:

    1. Unicode NFC normalisation (canonical composition).
    2. Replace common smart-quote / dash / invisible Unicode characters.
    3. Strip PDF header/footer artefacts (EU OJ-specific patterns).
    4. Rejoin hyphenated words split across lines.
    5. Normalise whitespace (tabs → spaces, trailing spaces, blank lines).
    """

    def normalize(self, text: str) -> str:
        """Return a cleaned version of *text*.

        Parameters
        ----------
        text:
            Raw text extracted by any ingestion method (PDF, HTML, OCR).

        Returns
        -------
        str
            Normalised text ready for the parsing stage.
        """
        if not text:
            return ""

        original_len = len(text)

        # 1. Unicode NFC normalisation
        text = unicodedata.normalize("NFC", text)

        # 2. Replace known smart-quote / invisible characters
        for old, new in _UNICODE_REPLACEMENTS.items():
            text = text.replace(old, new)

        # 3. Remove header / footer artefacts
        text = _HEADER_FOOTER_RE.sub("", text)

        # 4. Rejoin hyphenated line-breaks
        text = _HYPHEN_LINEBREAK_RE.sub(r"\1\2", text)

        # 5. Whitespace normalisation
        # Tabs → single space
        text = text.replace("\t", " ")
        # Trailing spaces on each line
        text = re.sub(r"[ ]+$", "", text, flags=re.MULTILINE)
        # Leading spaces on each line (keep indentation up to 3 spaces for lists)
        text = re.sub(r"^[ ]{4,}", "   ", text, flags=re.MULTILINE)
        # Collapse excessive blank lines
        text = _MULTI_BLANK_RE.sub("\n\n", text)
        # Strip leading/trailing whitespace from the whole document
        text = text.strip()

        logger.info(
            "Normalised text: %d → %d characters (%.1f%% reduction)",
            original_len,
            len(text),
            (1 - len(text) / original_len) * 100 if original_len else 0,
        )

        return text
