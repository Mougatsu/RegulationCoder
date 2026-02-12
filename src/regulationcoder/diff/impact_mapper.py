"""ImpactMapper — trace clause changes to impacted requirements and rules."""

import logging

from regulationcoder.models.diff import ChangeType, ClauseChange, ImpactedItem, SemanticChangeType
from regulationcoder.models.requirement import Requirement
from regulationcoder.models.rule import Rule

logger = logging.getLogger(__name__)

# Map semantic change types to default priority levels
_PRIORITY_BY_SEMANTIC: dict[SemanticChangeType | None, str] = {
    SemanticChangeType.SUBSTANTIVE: "high",
    SemanticChangeType.CLARIFICATION: "medium",
    SemanticChangeType.STRUCTURAL: "low",
    SemanticChangeType.EDITORIAL: "low",
    None: "medium",
}


class ImpactMapper:
    """Map clause-level changes to downstream requirements and rules.

    For each changed clause, the mapper:
    1. Finds all requirements whose ``clause_id`` matches the changed clause.
    2. For each impacted requirement, finds all rules whose ``requirement_id``
       matches the requirement.
    3. Produces an :class:`ImpactedItem` for every affected requirement and rule.
    """

    def map_impact(
        self,
        changes: list[ClauseChange],
        requirements: list[Requirement],
        rules: list[Rule],
    ) -> list[ImpactedItem]:
        """Return a list of ImpactedItem objects for all downstream artefacts.

        Only changes of type ADDED, DELETED, or MODIFIED are considered.
        UNCHANGED clauses are ignored.
        """
        # Build lookup indices
        reqs_by_clause: dict[str, list[Requirement]] = {}
        for req in requirements:
            reqs_by_clause.setdefault(req.clause_id, []).append(req)

        rules_by_req: dict[str, list[Rule]] = {}
        for rule in rules:
            rules_by_req.setdefault(rule.requirement_id, []).append(rule)

        impacted: list[ImpactedItem] = []
        seen_ids: set[str] = set()

        for change in changes:
            if change.change_type == ChangeType.UNCHANGED:
                continue

            priority = _PRIORITY_BY_SEMANTIC.get(change.semantic_type, "medium")
            needs_regen = change.change_type in (
                ChangeType.ADDED,
                ChangeType.DELETED,
            ) or change.semantic_type == SemanticChangeType.SUBSTANTIVE

            # Find impacted requirements
            affected_reqs = reqs_by_clause.get(change.clause_id, [])

            for req in affected_reqs:
                if req.id not in seen_ids:
                    seen_ids.add(req.id)
                    impacted.append(
                        ImpactedItem(
                            item_id=req.id,
                            item_type="requirement",
                            impact_description=(
                                f"Requirement derived from clause {change.clause_id} "
                                f"which was {change.change_type.value}."
                            ),
                            needs_regeneration=needs_regen,
                            priority=priority,
                        )
                    )

                # Find impacted rules for this requirement
                affected_rules = rules_by_req.get(req.id, [])
                for rule in affected_rules:
                    if rule.id not in seen_ids:
                        seen_ids.add(rule.id)
                        impacted.append(
                            ImpactedItem(
                                item_id=rule.id,
                                item_type="rule",
                                impact_description=(
                                    f"Rule derived from requirement {req.id}, "
                                    f"which traces back to clause {change.clause_id} "
                                    f"({change.change_type.value})."
                                ),
                                needs_regeneration=needs_regen,
                                priority=priority,
                            )
                        )

            # If no requirements map to this clause (e.g. new clause), still
            # record the clause-level impact.
            if not affected_reqs and change.change_type == ChangeType.ADDED:
                clause_item_id = f"clause:{change.clause_id}"
                if clause_item_id not in seen_ids:
                    seen_ids.add(clause_item_id)
                    impacted.append(
                        ImpactedItem(
                            item_id=clause_item_id,
                            item_type="requirement",
                            impact_description=(
                                f"New clause {change.clause_id} added — "
                                f"requirements need to be extracted."
                            ),
                            needs_regeneration=True,
                            priority="high",
                        )
                    )

        logger.info(
            "ImpactMapper: %d impacted items (%d requirements, %d rules)",
            len(impacted),
            sum(1 for i in impacted if i.item_type == "requirement"),
            sum(1 for i in impacted if i.item_type == "rule"),
        )
        return impacted
