"""Upload router — upload regulation documents for ingestion."""

import logging
import os
import tempfile
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, UploadFile
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["upload"])


class UploadResponse(BaseModel):
    """Response returned after a document upload."""
    status: str
    message: str
    file_name: str
    file_size: int
    clauses_extracted: int
    regulation_id: str
    version: str
    timestamp: str


@router.post("/", response_model=UploadResponse)
async def upload_regulation(
    file: UploadFile,
    request: Request,
    regulation_id: str = "custom-regulation",
    version: str = "v1",
):
    """Upload a regulation document (PDF or HTML) and trigger ingestion.

    The file is saved to a temporary location, then processed through the
    ingestion and parsing stages of the pipeline. Extracted clauses are
    added to the in-memory store.

    Query parameters:
    - regulation_id: identifier for the regulation (default: "custom-regulation")
    - version: document version string (default: "v1")
    """
    # Validate file type
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No filename provided")

    allowed_extensions = (".pdf", ".html", ".htm", ".txt")
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_ext}'. Allowed: {', '.join(allowed_extensions)}",
        )

    # Read file content
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    # Save to temporary file
    suffix = file_ext
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        from regulationcoder.core.pipeline import PipelineOrchestrator

        orchestrator = PipelineOrchestrator()

        # Run ingestion
        text = orchestrator.run_ingestion(tmp_path)

        # Run parsing
        clauses = orchestrator.run_parsing(text, regulation_id, version)

        # Add clauses to the in-memory store
        store = request.app.state.store
        for clause in clauses:
            store["clauses"][clause.id] = clause

        logger.info(
            "Uploaded and processed %s: %d clauses extracted",
            file.filename,
            len(clauses),
        )

        return UploadResponse(
            status="success",
            message=f"Document processed successfully. Extracted {len(clauses)} clauses.",
            file_name=file.filename,
            file_size=len(content),
            clauses_extracted=len(clauses),
            regulation_id=regulation_id,
            version=version,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        logger.exception("Error processing uploaded document")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}",
        )
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
