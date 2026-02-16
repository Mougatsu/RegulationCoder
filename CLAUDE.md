# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

```bash
# Install Python package (editable)
pip install -e .
pip install -e ".[dev]"          # with dev dependencies (pytest, ruff, mypy)

# Backend (FastAPI on port 8000)
uvicorn regulationcoder.api.app:app --host 0.0.0.0 --port 8000 --reload

# Frontend (Next.js on port 3000)
cd dashboard && npm install && npm run dev

# Docker (PostgreSQL + FastAPI)
docker-compose up

# CLI
regulationcoder check --profile tests/fixtures/talentscreen_profile.json --regulation eu-ai-act-v1
regulationcoder verify-audit --log-dir ./audit_logs

# Demo pipeline
python scripts/run_demo_pipeline.py
```

### Testing & Quality

```bash
pytest                                    # all tests
pytest tests/unit/test_engine.py -v       # single test file
pytest --cov=regulationcoder              # with coverage
ruff check src/                           # lint
mypy src/                                 # type check (strict mode)
```

## Architecture

**RegulationCoder** converts regulation documents (PDF/HTML) into working compliance software using a multi-stage pipeline, then evaluates AI systems against the generated rules.

### Pipeline Stages

1. **Ingestion** (`ingestion/`) — PDF/HTML → raw text (PyPDF2, pdfplumber, BeautifulSoup, OCR fallback)
2. **Parsing** (`parser/`) — raw text → hierarchical clauses with deterministic IDs
3. **Extraction** (`extraction/`) — clauses → requirements via Claude Sonnet 4.5, validated by Judge Gate A (Claude Opus 4.6)
4. **Formalization** (`formalization/`) — requirements → executable rules via Claude Sonnet 4.5, validated by Judge Gate B (Claude Opus 4.6)
5. **Evaluation** (`core/engine.py`) — deterministic rule engine evaluates a `SystemProfile` against rules, produces `ComplianceReport`
6. **AI Analysis** (`core/ai_analyzer.py`) — Claude Opus 4.6 provides contextual risk narrative, insights, and prioritized actions on top of the deterministic report
7. **Export** (`exporters/`) — JSON, HTML (Jinja2), PDF (WeasyPrint)

### Dual-Model Strategy

- **Claude Sonnet 4.5**: extraction and formalization (fast, cost-effective)
- **Claude Opus 4.6**: judge gates, deep analysis (quality assurance, contextual reasoning)

### Key Design Patterns

- **Judge Gates**: Opus validates Sonnet outputs before they're stored; ensures extraction/formalization quality
- **Deterministic + AI Hybrid**: fast rule engine for scoring, optional AI analysis for depth
- **Hash-chained audit trail** (`audit/`): SHA-256 append-only JSONL log; each entry references previous hash
- **In-memory store for MVP**: pre-loaded EU AI Act data (Articles 9-15, 53 rules); PostgreSQL models exist but aren't active

### Pre-built Regulation Data

`src/regulationcoder/rules/eu_ai_act_v1/` contains fully codified EU AI Act Articles 9-15 as Python objects with evaluation functions. Each `art*.py` file exports clauses, requirements, and rules for one article. The `mapping.py` file connects articles to rules.

### Rule Evaluation Flow

Rules in `models/rule.py` have `inputs_needed` (dotted field paths into `SystemProfile`) and `evaluation_logic`. The engine (`core/engine.py`) resolves fields, tries named evaluation functions from the rule module first, falls back to `exec()` of the logic string. Verdicts: PASS, FAIL, NOT_APPLICABLE, MANUAL_REVIEW. Score = passed/applicable * 100.

### API Layer

FastAPI app in `api/app.py` with routers under `api/routers/`. Key endpoints: `POST /api/evaluate/` (deterministic), `POST /api/evaluate/ai-analysis` (Claude Opus, ~60-90s), plus CRUD for regulations/requirements/rules/audit. WebSocket at `/ws/pipeline` for progress. CORS open for development.

### Dashboard

Next.js 14 app in `dashboard/` using Tailwind CSS, shadcn/ui, and Recharts. Typed API client in `dashboard/src/lib/api.ts`. Main page is `/evaluate` which loads demo profiles and triggers evaluation.

## Configuration

Environment variables (`.env` file): `ANTHROPIC_API_KEY`, `EXTRACTION_MODEL`, `JUDGE_MODEL`, `DATABASE_URL`, `AUDIT_LOG_DIR`, `MAX_JUDGE_RETRIES`, `JUDGE_TIMEOUT`, `BATCH_SIZE`. Settings loaded in `core/config.py`.

## Code Conventions

- Python 3.12+, Pydantic v2 models throughout
- Ruff for linting (rules: E, F, I, N, W), line length 100
- mypy strict mode
- pytest with `asyncio_mode = "auto"`
- Package source in `src/regulationcoder/`, built with hatchling
