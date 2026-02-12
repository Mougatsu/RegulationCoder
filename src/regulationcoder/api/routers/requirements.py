"""Requirements router — endpoints for querying extracted requirements."""

from fastapi import APIRouter, HTTPException, Query, Request

from regulationcoder.models.requirement import Requirement

router = APIRouter(prefix="/api/requirements", tags=["requirements"])


@router.get("/", response_model=list[Requirement])
async def list_requirements(
    request: Request,
    regulation_id: str | None = Query(None, description="Filter by regulation ID"),
):
    """List all requirements, optionally filtered by regulation_id.

    The regulation_id filter matches against the clause_id prefix, since
    requirements reference clauses which belong to a regulation.
    """
    store = request.app.state.store
    requirements = list(store["requirements"].values())

    if regulation_id:
        # Clause IDs start with the regulation ID, e.g. "eu-ai-act-v1/art10/..."
        # Match if the clause_id starts with the regulation_id
        requirements = [
            req
            for req in requirements
            if req.clause_id.startswith(regulation_id)
        ]

    return requirements


@router.get("/{requirement_id}", response_model=Requirement)
async def get_requirement(requirement_id: str, request: Request):
    """Get a specific requirement by ID."""
    store = request.app.state.store
    req = store["requirements"].get(requirement_id)
    if req is None:
        raise HTTPException(
            status_code=404, detail=f"Requirement '{requirement_id}' not found"
        )
    return req
