"""MappingGenerator — creates article-to-rule traceability mappings."""

import logging
from collections import defaultdict

from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)


class MappingGenerator:
    """Generate traceability mapping from articles to rules and requirements.

    This is a deterministic generator that creates a structured mapping table
    linking regulation articles to their derived rules and requirements.

    Usage:
        generator = MappingGenerator()
        mapping = generator.generate(rules, requirements)
    """

    def generate(
        self, rules: list[Rule], requirements: list[Requirement]
    ) -> dict:
        """Create an Article -> Rule ID -> Requirement ID mapping table.

        Args:
            rules: List of Rule objects.
            requirements: List of Requirement objects.

        Returns:
            A structured dict with the following shape:
            {
                "metadata": {
                    "total_articles": int,
                    "total_requirements": int,
                    "total_rules": int,
                },
                "articles": {
                    "Article 10": {
                        "article_ref": "Article 10",
                        "requirements": [
                            {
                                "requirement_id": "REQ-...",
                                "modality": "must",
                                "subject": "...",
                                "action": "...",
                                "rules": [
                                    {
                                        "rule_id": "RULE-...",
                                        "rule_type": "automated",
                                        "severity": "high",
                                        "title": "...",
                                    }
                                ]
                            }
                        ]
                    }
                },
                "rule_to_requirement": { "RULE-...": "REQ-..." },
                "requirement_to_clause": { "REQ-...": "clause-id" },
            }
        """
        # Index requirements by ID
        req_by_id: dict[str, Requirement] = {r.id: r for r in requirements}

        # Index rules by requirement ID
        rules_by_req: dict[str, list[Rule]] = defaultdict(list)
        for rule in rules:
            rules_by_req[rule.requirement_id].append(rule)

        # Group requirements by article reference
        article_groups: dict[str, list[Requirement]] = defaultdict(list)
        for req in requirements:
            article_ref = self._extract_article_ref(req)
            article_groups[article_ref].append(req)

        # Build the mapping structure
        articles_map: dict[str, dict] = {}
        for article_ref in sorted(article_groups.keys()):
            reqs = article_groups[article_ref]
            req_entries = []
            for req in reqs:
                associated_rules = rules_by_req.get(req.id, [])
                rule_entries = [
                    {
                        "rule_id": rule.id,
                        "rule_type": rule.rule_type.value,
                        "severity": rule.severity.value,
                        "title": rule.title,
                    }
                    for rule in associated_rules
                ]
                req_entries.append(
                    {
                        "requirement_id": req.id,
                        "modality": req.modality.value,
                        "subject": req.subject,
                        "action": req.action,
                        "object": req.object,
                        "scope": req.scope,
                        "rules": rule_entries,
                    }
                )
            articles_map[article_ref] = {
                "article_ref": article_ref,
                "requirements": req_entries,
            }

        # Build reverse mappings
        rule_to_requirement = {rule.id: rule.requirement_id for rule in rules}
        requirement_to_clause = {req.id: req.clause_id for req in requirements}

        mapping = {
            "metadata": {
                "total_articles": len(articles_map),
                "total_requirements": len(requirements),
                "total_rules": len(rules),
            },
            "articles": articles_map,
            "rule_to_requirement": rule_to_requirement,
            "requirement_to_clause": requirement_to_clause,
        }

        logger.info(
            "Generated mapping: %d articles, %d requirements, %d rules",
            len(articles_map),
            len(requirements),
            len(rules),
        )

        return mapping

    @staticmethod
    def _extract_article_ref(requirement: Requirement) -> str:
        """Extract the article reference string from a requirement's citations.

        Falls back to parsing the requirement ID if no citations are present.
        """
        # Try citations first
        if requirement.citations:
            ref = requirement.citations[0].article_ref
            if ref:
                return ref

        # Fall back to parsing the requirement ID
        # Format: REQ-EU-AI-ACT-{art:03d}-{para:02d}{sub}-{seq:03d}
        parts = requirement.id.split("-")
        if len(parts) >= 5:
            try:
                art_num = int(parts[4])
                return f"Article {art_num}"
            except ValueError:
                pass

        return "Unknown Article"
