"""FastAPI application for RegulationCoder."""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from regulationcoder.api.routers import audit, evaluate, regulations, requirements, rules, upload

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory data store (populated at startup from pre-built regulation data)
# ---------------------------------------------------------------------------
# These dictionaries are shared across routers via app.state.
# For the MVP this replaces a database.

_store: dict = {
    "regulations": {},
    "clauses": {},
    "requirements": {},
    "rules": {},
    "reports": {},
    "audit_entries": [],
}


def _bootstrap_eu_ai_act(store: dict) -> None:
    """Pre-load the EU AI Act data into the in-memory store."""
    from regulationcoder.rules.eu_ai_act_v1 import (
        get_clauses,
        get_regulation,
        get_requirements,
        get_rules,
    )

    reg = get_regulation()
    store["regulations"][reg.id] = reg

    for clause in get_clauses():
        store["clauses"][clause.id] = clause

    for req in get_requirements():
        store["requirements"][req.id] = req

    for rule in get_rules():
        store["rules"][rule.id] = rule

    logger.info(
        "Bootstrapped EU AI Act: %d clauses, %d requirements, %d rules",
        len(store["clauses"]),
        len(store["requirements"]),
        len(store["rules"]),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — load seed data on startup."""
    _bootstrap_eu_ai_act(_store)
    app.state.store = _store
    logger.info("RegulationCoder API started")
    yield
    logger.info("RegulationCoder API shutting down")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="RegulationCoder API",
    description=(
        "End-to-end pipeline converting regulation documents into compliance "
        "software. Evaluate AI system profiles against the EU AI Act and other "
        "regulations."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(regulations.router)
app.include_router(requirements.router)
app.include_router(rules.router)
app.include_router(evaluate.router)
app.include_router(upload.router)
app.include_router(audit.router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "RegulationCoder API",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# WebSocket endpoint for pipeline progress
# ---------------------------------------------------------------------------

class PipelineConnectionManager:
    """Manages active WebSocket connections for pipeline progress streaming."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_progress(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                pass


pipeline_manager = PipelineConnectionManager()


@app.websocket("/ws/pipeline")
async def websocket_pipeline(websocket: WebSocket):
    """WebSocket endpoint for streaming pipeline progress updates.

    Clients connect to receive real-time updates as regulation documents
    are processed through the ingestion pipeline stages.

    Messages sent to the client follow this format:
    {
        "stage": "ingestion" | "parsing" | "extraction" | "formalization" | "codegen",
        "status": "started" | "progress" | "completed" | "error",
        "progress": 0-100,
        "message": "Human-readable status message",
        "details": { ... }
    }
    """
    await pipeline_manager.connect(websocket)
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "stage": "connection",
            "status": "connected",
            "progress": 0,
            "message": "Connected to pipeline progress stream",
        })

        # Keep connection alive and listen for client messages
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Echo back acknowledgment
                await websocket.send_json({
                    "stage": "connection",
                    "status": "acknowledged",
                    "message": f"Received: {data}",
                })
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({
                    "stage": "connection",
                    "status": "heartbeat",
                    "progress": 0,
                    "message": "Connection alive",
                })
    except WebSocketDisconnect:
        pipeline_manager.disconnect(websocket)
    except Exception:
        pipeline_manager.disconnect(websocket)
