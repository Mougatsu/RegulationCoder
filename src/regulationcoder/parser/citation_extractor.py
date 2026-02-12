"""Citation extractor — finds cross-references to other articles/paragraphs.

EU regulation texts are full of internal references like:

- "referred to in Article 6(1)"
- "in accordance with Article 9(2), point (a)"
- "as defined in Article 3, point (44)"
- "pursuant to paragraph 3"
- "Article 52(1) and (2)"
"""

import logging
import re

from regulationcoder.core.exceptions import ParsingError
from regulationcoder.models.citation import Citation

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Regex patterns for EU-style cross-references
# ---------------------------------------------------------------------------

# Full article reference with optional paragraph and subsection:
#   "Article 6"
#   "Article 6(1)"
#   "Article 6(1)(a)"
#   "Article 6(1), point (a)"
#   "Articles 6 and 7"     (captures first article only per match)
_ARTICLE_REF_RE = re.compile(
    r"(?:Article|article|ARTICLE)s?\s+"
    r"(\d+)"                                   # article number
    r"(?:\((\d+)\))?"                           # optional paragraph in parens
    r"(?:"
    r"\(([a-z])\)"                             # optional subsection in parens
    r"|"
    r",?\s*point\s+\(([a-z])\)"               # or "point (x)"
    r")?"
)

# "paragraph N" or "paragraphs N and M" — relative reference within the
# same article.
_PARAGRAPH_REF_RE = re.compile(
    r"(?:paragraph|Paragraph|PARAGRAPH)s?\s+(\d+)"
)

# "point (a)" without a preceding Article reference — relative to the
# current paragraph.
_POINT_REF_RE = re.compile(
    r"(?<!\()\bpoints?\s+\(([a-z])\)"
)


class CitationExtractor:
    """Extract cross-reference :class:`Citation` objects from clause text."""

    def extract(self, text: str, clause_id: str) -> list[Citation]:
        """Find all regulation cross-references in *text*.

        Parameters
        ----------
        text:
            The text of a single clause (or any regulation text).
        clause_id:
            The deterministic ID of the clause being analysed, used as
            the ``clause_id`` field on each returned :class:`Citation`.

        Returns
        -------
        list[Citation]
            One :class:`Citation` per unique reference found.  Duplicates
            (same article + paragraph + subsection) are removed.

        Raises
        ------
        ParsingError
            If the text is ``None``.
        """
        if text is None:
            raise ParsingError("Cannot extract citations from None text")

        if not text.strip():
            return []

        citations: list[Citation] = []
        seen: set[tuple[str, str | None, str | None]] = set()

        # --- Full Article references ---
        for m in _ARTICLE_REF_RE.finditer(text):
            article_num = m.group(1)
            paragraph_num = m.group(2)  # may be None
            subsection = m.group(3) or m.group(4)  # may be None

            article_ref = f"Article {article_num}"
            key = (article_ref, paragraph_num, subsection)
            if key in seen:
                continue
            seen.add(key)

            # Extract a surrounding context window as the exact quote.
            quote = self._context_window(text, m.start(), m.end())

            citations.append(
                Citation(
                    clause_id=clause_id,
                    article_ref=article_ref,
                    paragraph_ref=paragraph_num,
                    subsection_ref=subsection,
                    exact_quote=quote,
                )
            )

        # --- Relative paragraph references ---
        for m in _PARAGRAPH_REF_RE.finditer(text):
            paragraph_num = m.group(1)

            # Derive the article reference from the clause_id.
            article_ref = self._article_ref_from_clause_id(clause_id)
            key = (article_ref, paragraph_num, None)
            if key in seen:
                continue
            seen.add(key)

            quote = self._context_window(text, m.start(), m.end())

            citations.append(
                Citation(
                    clause_id=clause_id,
                    article_ref=article_ref,
                    paragraph_ref=paragraph_num,
                    exact_quote=quote,
                )
            )

        # --- Relative point references (within same paragraph) ---
        for m in _POINT_REF_RE.finditer(text):
            subsection = m.group(1)

            article_ref = self._article_ref_from_clause_id(clause_id)
            para_ref = self._paragraph_ref_from_clause_id(clause_id)
            key = (article_ref, para_ref, subsection)
            if key in seen:
                continue
            seen.add(key)

            quote = self._context_window(text, m.start(), m.end())

            citations.append(
                Citation(
                    clause_id=clause_id,
                    article_ref=article_ref,
                    paragraph_ref=para_ref,
                    subsection_ref=subsection,
                    exact_quote=quote,
                )
            )

        logger.info(
            "Extracted %d citation(s) from clause %s",
            len(citations),
            clause_id,
        )
        return citations

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _context_window(text: str, start: int, end: int, margin: int = 60) -> str:
        """Return text around the match with *margin* characters on each side."""
        ctx_start = max(0, start - margin)
        ctx_end = min(len(text), end + margin)
        snippet = text[ctx_start:ctx_end].strip()
        # Replace internal newlines with spaces for a cleaner quote.
        return re.sub(r"\s+", " ", snippet)

    @staticmethod
    def _article_ref_from_clause_id(clause_id: str) -> str:
        """Extract an ``Article N`` string from a deterministic clause ID.

        E.g. ``"eu-ai-act-v1/art10/para2"`` → ``"Article 10"``.
        """
        art_match = re.search(r"/art(\d+)", clause_id)
        if art_match:
            return f"Article {art_match.group(1)}"
        return "Article ?"

    @staticmethod
    def _paragraph_ref_from_clause_id(clause_id: str) -> str | None:
        """Extract a paragraph number from a clause ID, if present.

        E.g. ``"eu-ai-act-v1/art10/para2/sub-f"`` → ``"2"``.
        """
        para_match = re.search(r"/para(\d+)", clause_id)
        if para_match:
            return para_match.group(1)
        return None
