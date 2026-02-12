"""Regulations router — CRUD endpoints for regulation data."""

from fastapi import APIRouter, HTTPException, Request

from regulationcoder.models.clause import Clause
from regulationcoder.models.regulation import Regulation

router = APIRouter(prefix="/api/regulations", tags=["regulations"])


@router.get("/", response_model=list[Regulation])
async def list_regulations(request: Request):
    """List all available regulations."""
    store = request.app.state.store
    return list(store["regulations"].values())


@router.get("/{regulation_id}", response_model=Regulation)
async def get_regulation(regulation_id: str, request: Request):
    """Get details of a specific regulation."""
    store = request.app.state.store
    reg = store["regulations"].get(regulation_id)
    if reg is None:
        raise HTTPException(status_code=404, detail=f"Regulation '{regulation_id}' not found")
    return reg


@router.get("/{regulation_id}/clauses", response_model=list[Clause])
async def list_clauses(regulation_id: str, request: Request):
    """List all clauses for a regulation."""
    store = request.app.state.store

    # Verify the regulation exists
    if regulation_id not in store["regulations"]:
        raise HTTPException(status_code=404, detail=f"Regulation '{regulation_id}' not found")

    clauses = [
        clause
        for clause in store["clauses"].values()
        if clause.regulation_id == regulation_id
    ]
    return clauses


@router.get("/{regulation_id}/clauses/{clause_id:path}", response_model=Clause)
async def get_clause(regulation_id: str, clause_id: str, request: Request):
    """Get a specific clause by ID."""
    store = request.app.state.store

    if regulation_id not in store["regulations"]:
        raise HTTPException(status_code=404, detail=f"Regulation '{regulation_id}' not found")

    clause = store["clauses"].get(clause_id)
    if clause is None:
        raise HTTPException(status_code=404, detail=f"Clause '{clause_id}' not found")

    if clause.regulation_id != regulation_id:
        raise HTTPException(
            status_code=404,
            detail=f"Clause '{clause_id}' does not belong to regulation '{regulation_id}'",
        )

    return clause
