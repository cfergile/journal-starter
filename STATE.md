# Project state — journal-starter

*Last updated: 2025-09-02*

## Snapshot
* Guide: https://learntocloud.guide/phase2/build-app
* Stack: FastAPI (async) • SQLAlchemy ORM (async) • PostgreSQL • Alembic • Pydantic v2 • pytest (AsyncClient + mocks)
* Pattern: Service–repository • Dependency-injected routes
* Tooling: Ruff • Black • isort • mypy • GitHub Actions CI + Codecov • Bandit • Trivy (FS scan) • Dependabot
* Deploy: **Render (free tier)** — https://journal-starter.onrender.com

## Progress
1. Scaffolding & repo setup — ✅ Complete  
2. Environment & .env config — ✅ Complete (`.env` + `.env.example` aligned; `app/core/config.py` wired)  
3. DB model & Alembic migration — ✅ Complete (entry table; head `73f82b54943b`)  
4. SQLAlchemy async integration — ✅ Complete  
5. Pydantic v2 schemas — ✅ Complete (ConfigDict + `model_validate`)  
6. Service/repository layer — ✅ Complete  
7. API routing (CRUD) — ✅ Complete (create/get/update/delete/list)  
8. Dependency injection — ✅ Complete (overrides testable)  
9. Router unit tests (mocked service) — ✅ Complete  
10. Service-layer unit tests — ✅ Complete (CRUD + edge cases)  
11. Integration tests (real DB) — ✅ Complete (green locally & in CI)  
12. API docs (OpenAPI) — ✅ Complete (FastAPI default)  
13. CORS, logging, healthcheck — ✅ Complete  
14. CI quality gates — ✅ Complete (Ruff + Black + mypy + Bandit + **Trivy passing**)  
15. README polish — ✅ Updated (quickstart, env, CI gates, Render demo)  
16. Deployment — ✅ **Render** live

## Current step
* Optional: add AWS deploy manifest to showcase multi-cloud.
* Optional: monitoring/logging notes for Render.
* Prep `v1.0.0` tag.

## Test status
* Summary: **24 passed** locally (`pytest -q` on 2025-09-02); **24 passed** in CI.
* Coverage: ~90%+ (threshold enforced).
* Notable failures/flakes: none.

## Database & migrations
* Local DB: Postgres 16 @ localhost:5432  
* Render DB: Postgres add-on linked to service  
* Alembic head: **73f82b54943b** (`add_entry_table`)  
* `alembic current`: ✅ matches head  
* Pending migrations: **0**  
* CI DB: GitHub Actions Postgres service

## Open issues / TODOs
* [ ] Optional: AWS deploy (ECS/Fargate or App Runner) docs.
* [ ] Optional: performance/load tests.
* [ ] Optional: add SLOs + health/metrics notes.

## Next actions (concrete)
1. Add small “Ops” section to README (alerts/monitoring ideas).
2. Optionally add AWS IaC snippet (Terraform/App Runner) for recruiters.
3. Tag **v1.0.0**.
