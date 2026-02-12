"""EU AI Act v1 -- seed data for Articles 9-15 (Chapter III, Section 2).

This package provides pre-built clauses, requirements, rules and evaluation
functions derived from the EU Artificial Intelligence Act (Regulation 2024/1689).

Exports
-------
get_regulation()           -> Regulation
get_clauses()              -> list[Clause]
get_requirements()         -> list[Requirement]
get_rules()                -> list[Rule]
get_evaluation_function()  -> Callable | None
"""

from collections.abc import Callable

from regulationcoder.models.clause import Clause
from regulationcoder.models.regulation import Regulation
from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule

from regulationcoder.rules.eu_ai_act_v1 import (
    art09,
    art10,
    art11,
    art12,
    art13,
    art14,
    art15,
)

_ARTICLE_MODULES = [art09, art10, art11, art12, art13, art14, art15]


def get_regulation() -> Regulation:
    """Return the EU AI Act regulation metadata."""
    return Regulation(
        id="eu-ai-act",
        title="Regulation (EU) 2024/1689 -- Artificial Intelligence Act",
        short_name="EU AI Act",
        document_version="2024-1689-oj",
        jurisdiction="European Union",
        language="en",
        source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        total_articles=113,
        total_clauses=len(get_clauses()),
    )


def get_clauses() -> list[Clause]:
    """Return all clauses from Articles 9-15."""
    clauses: list[Clause] = []
    for mod in _ARTICLE_MODULES:
        clauses.extend(mod.CLAUSES)
    return clauses


def get_requirements() -> list[Requirement]:
    """Return all requirements from Articles 9-15."""
    requirements: list[Requirement] = []
    for mod in _ARTICLE_MODULES:
        requirements.extend(mod.REQUIREMENTS)
    return requirements


def get_rules() -> list[Rule]:
    """Return all rules from Articles 9-15."""
    rules: list[Rule] = []
    for mod in _ARTICLE_MODULES:
        rules.extend(mod.RULES)
    return rules


def get_evaluation_function(rule_id: str) -> Callable[..., str] | None:
    """Look up the Python evaluation function for a given rule ID.

    Returns ``None`` if no function is registered for the rule.
    """
    for mod in _ARTICLE_MODULES:
        fn = mod.EVALUATION_FUNCTIONS.get(rule_id)
        if fn is not None:
            return fn
    return None
