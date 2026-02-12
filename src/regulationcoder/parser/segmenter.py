"""Clause segmenter for EU-style regulation documents.

Splits the normalised full text of a regulation into individual
:class:`~regulationcoder.models.clause.Clause` objects using regex
patterns that match the standard EU legislation structure:

- **Articles**  -- ``Article 1``, ``Article 2``, ...
- **Paragraphs** -- leading ``1.``, ``2.``, ... (numbered paragraphs)
- **Subsections** -- ``(a)``, ``(b)``, ... or ``(i)``, ``(ii)``, ...
"""

import logging
import re

from regulationcoder.core.exceptions import ParsingError
from regulationcoder.models.clause import Clause

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Regex patterns for EU legislation structure
# ---------------------------------------------------------------------------

# "Article 10" or "ARTICLE 10" at the start of a line.
_ARTICLE_HEADING_RE = re.compile(
    r"^(?:Article|ARTICLE)\s+(\d+)\b",
    re.MULTILINE,
)

# Numbered paragraph at the start of a line: "1. ...", "12. ..."
# Anchored to start-of-string or after a newline.
_PARAGRAPH_START_RE = re.compile(
    r"(?:^|\n)(?=(\d+)\.\s)",
)

# Subsection letter at the start of a line or after whitespace: "(a) ..."
_SUBSECTION_START_RE = re.compile(
    r"(?:^|\n)\(([a-z])\)\s",
)


def _make_clause_id(
    regulation_id: str,
    document_version: str,
    article: int,
    paragraph: int | None = None,
    subsection: str | None = None,
) -> str:
    """Build a deterministic clause ID.

    Examples::

        eu-ai-act/art10
        eu-ai-act/art10/para2
        eu-ai-act/art10/para2/sub-f
    """
    parts = [f"{regulation_id}/art{article}"]
    if paragraph is not None:
        parts.append(f"para{paragraph}")
    if subsection is not None:
        parts.append(f"sub-{subsection}")
    return "/".join(parts)


def _split_at_pattern(text: str, pattern: re.Pattern) -> list[tuple[str, int, str]]:
    """Split *text* at every position where *pattern* matches.

    Returns a list of ``(captured_group_1, start_offset, body_text)``
    tuples.  The *body_text* runs from just after the match to the start
    of the next match (or end-of-string).

    The first capture group of *pattern* must contain the identifier
    (article number, paragraph number, or subsection letter).
    """
    matches = list(pattern.finditer(text))
    if not matches:
        return []

    results: list[tuple[str, int, str]] = []
    for i, m in enumerate(matches):
        identifier = m.group(1)
        # Body starts after the full prefix (e.g. after "1. " or "(a) ").
        # We need to find the end of the prefix on this line.
        prefix_end = m.end()
        # For paragraph pattern, the body starts after "N. "
        body_start = prefix_end
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        results.append((identifier, m.start(), body))

    return results


class ClauseSegmenter:
    """Segment regulation text into a flat list of :class:`Clause` objects."""

    def segment(
        self,
        text: str,
        regulation_id: str,
        document_version: str,
    ) -> list[Clause]:
        """Parse *text* and return one :class:`Clause` per structural element.

        Parameters
        ----------
        text:
            Full normalised text of the regulation document.
        regulation_id:
            Short identifier for the regulation (e.g. ``"eu-ai-act"``).
        document_version:
            Version string (e.g. ``"v1"`` or ``"2024-1689-oj"``).

        Returns
        -------
        list[Clause]
            Flat list of clauses ordered by their position in the text.
            Parent-child relationships are encoded via ``parent_clause_id``.

        Raises
        ------
        ParsingError
            If no articles can be identified in the text.
        """
        if not text or not text.strip():
            raise ParsingError("Cannot segment empty text")

        clauses: list[Clause] = []

        # 1. Find all Article boundaries.
        article_matches = list(_ARTICLE_HEADING_RE.finditer(text))
        if not article_matches:
            raise ParsingError(
                "No Article headings found in text.  "
                "Ensure the input follows EU legislation structure."
            )

        logger.info("Found %d article(s) in text", len(article_matches))

        for idx, a_match in enumerate(article_matches):
            article_number = int(a_match.group(1))

            # Text span belonging to this article.
            art_start = a_match.end()  # skip past the "Article N" heading
            art_end = (
                article_matches[idx + 1].start()
                if idx + 1 < len(article_matches)
                else len(text)
            )
            article_text = text[art_start:art_end].strip()

            article_id = _make_clause_id(regulation_id, document_version, article_number)

            # Create the article-level clause (contains the full text).
            clauses.append(
                Clause(
                    id=article_id,
                    regulation_id=regulation_id,
                    document_version=document_version,
                    article_number=article_number,
                    text=article_text,
                    parent_clause_id=None,
                )
            )

            # 2. Split article body into numbered paragraphs.
            paragraphs = self._extract_paragraphs(article_text)

            if paragraphs:
                for para_num, para_text in paragraphs:
                    para_id = _make_clause_id(
                        regulation_id, document_version, article_number, para_num
                    )
                    clauses.append(
                        Clause(
                            id=para_id,
                            regulation_id=regulation_id,
                            document_version=document_version,
                            article_number=article_number,
                            paragraph_number=para_num,
                            text=para_text,
                            parent_clause_id=article_id,
                        )
                    )

                    # 3. Split each paragraph into subsections.
                    subsections = self._extract_subsections(para_text)
                    for sub_letter, sub_text in subsections:
                        sub_id = _make_clause_id(
                            regulation_id,
                            document_version,
                            article_number,
                            para_num,
                            sub_letter,
                        )
                        clauses.append(
                            Clause(
                                id=sub_id,
                                regulation_id=regulation_id,
                                document_version=document_version,
                                article_number=article_number,
                                paragraph_number=para_num,
                                subsection_letter=sub_letter,
                                text=sub_text,
                                parent_clause_id=para_id,
                            )
                        )
            else:
                # No numbered paragraphs -- check for subsections directly.
                subsections = self._extract_subsections(article_text)
                for sub_letter, sub_text in subsections:
                    sub_id = _make_clause_id(
                        regulation_id,
                        document_version,
                        article_number,
                        None,
                        sub_letter,
                    )
                    clauses.append(
                        Clause(
                            id=sub_id,
                            regulation_id=regulation_id,
                            document_version=document_version,
                            article_number=article_number,
                            subsection_letter=sub_letter,
                            text=sub_text,
                            parent_clause_id=article_id,
                        )
                    )

        logger.info("Segmented text into %d clause(s)", len(clauses))
        return clauses

    # ------------------------------------------------------------------
    # Internal splitting helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_paragraphs(article_text: str) -> list[tuple[int, str]]:
        """Extract numbered paragraphs from article body text.

        Returns list of ``(paragraph_number, paragraph_text)`` pairs.
        """
        # Find all "N. " patterns at the start of a line.
        para_re = re.compile(r"(?:^|\n)(\d+)\.\s+", re.MULTILINE)
        matches = list(para_re.finditer(article_text))

        if not matches:
            return []

        results: list[tuple[int, str]] = []
        for i, m in enumerate(matches):
            para_num = int(m.group(1))
            body_start = m.end()
            body_end = matches[i + 1].start() if i + 1 < len(matches) else len(article_text)
            body = article_text[body_start:body_end].strip()
            results.append((para_num, body))

        return results

    @staticmethod
    def _extract_subsections(text: str) -> list[tuple[str, str]]:
        """Extract lettered subsections from paragraph text.

        Returns list of ``(letter, subsection_text)`` pairs.
        """
        sub_re = re.compile(r"(?:^|\n)\(([a-z])\)\s+", re.MULTILINE)
        matches = list(sub_re.finditer(text))

        if not matches:
            return []

        results: list[tuple[str, str]] = []
        for i, m in enumerate(matches):
            letter = m.group(1)
            body_start = m.end()
            body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[body_start:body_end].strip()
            results.append((letter, body))

        return results
