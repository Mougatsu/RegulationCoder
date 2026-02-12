"""Mapping from EU AI Act article numbers to rule IDs.

This module provides a quick lookup so that callers can retrieve which
rules apply to a given article without iterating the full rule list.
"""

from regulationcoder.rules.eu_ai_act_v1 import (
    art09,
    art10,
    art11,
    art12,
    art13,
    art14,
    art15,
)

# ---------------------------------------------------------------------------
# Article -> Rule-ID mapping  (built from the article modules)
# ---------------------------------------------------------------------------
ARTICLE_RULE_MAPPING: dict[int, list[str]] = {
    9: [r.id for r in art09.RULES],
    10: [r.id for r in art10.RULES],
    11: [r.id for r in art11.RULES],
    12: [r.id for r in art12.RULES],
    13: [r.id for r in art13.RULES],
    14: [r.id for r in art14.RULES],
    15: [r.id for r in art15.RULES],
}


def get_rules_for_article(article_number: int) -> list[str]:
    """Return the list of rule IDs that correspond to a given article number.

    Parameters
    ----------
    article_number:
        The EU AI Act article number (9-15 supported).

    Returns
    -------
    list[str]
        Rule IDs for the requested article, or an empty list if the article
        is not covered.
    """
    return ARTICLE_RULE_MAPPING.get(article_number, [])
