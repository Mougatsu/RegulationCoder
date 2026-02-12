"""Rules router — endpoints for querying formalized compliance rules."""

from fastapi import APIRouter, HTTPException, Query, Request

from regulationcoder.models.rule import Rule

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("/", response_model=list[Rule])
async def list_rules(
    request: Request,
    regulation_id: str | None = Query(None, description="Filter by regulation ID"),
):
    """List all rules, optionally filtered by regulation_id.

    The regulation_id filter matches against the rule ID prefix. For example,
    rules for the EU AI Act have IDs like ``RULE-EU-AI-ACT-...``.
    """
    store = request.app.state.store
    all_rules = list(store["rules"].values())

    if regulation_id:
        # Normalize: "eu-ai-act" -> "EU-AI-ACT" for matching rule ID prefix
        normalized = regulation_id.upper().replace("-", "-")
        all_rules = [
            rule
            for rule in all_rules
            if normalized in rule.id.upper()
        ]

    return all_rules


@router.get("/{rule_id}", response_model=Rule)
async def get_rule(rule_id: str, request: Request):
    """Get a specific rule by ID."""
    store = request.app.state.store
    rule = store["rules"].get(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")
    return rule
