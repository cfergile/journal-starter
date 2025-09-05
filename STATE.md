# Project state — journal-starter

*Last updated: 2025-09-04*

## Snapshot
* Guide: https://learntocloud.guide/phase2/build-app
* Stack: FastAPI (async) • SQLAlchemy ORM (async) • PostgreSQL • Alembic • Pydantic v2 • pytest (AsyncClient + mocks)
* Pattern: Service–repository • Dependency-injected routes
* Tooling: Ruff • Black • isort • mypy • GitHub Actions CI + Codecov • Bandit • Trivy (FS scan) • Dependabot
* Ops: `/healthz` • optional `/metrics` (Prometheus) • env-driven LOG_LEVEL/SENTRY • GitHub Actions uptime workflow (warm-up + retries + Slack alerts)
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
13. CORS, logging, healthcheck — ✅ Complete (`/healthz`)  
14. CI quality gates — ✅ Complete (Ruff + Black + mypy + Bandit + **Trivy passing**)  
15. README polish — ✅ Updated (quickstart, env, CI gates, Render demo + uptime badge)  
16. Deployment — ✅ **Render** live (blueprint with `healthCheckPath: /healthz`, post-deploy `alembic upgrade head`)  
17. **Ops & Monitoring** — ✅ `/metrics` (Prometheus) optional; **uptime workflow** (30-min cron) with warm-up + retries + Slack alerts  
18. **k6** — ✅ Smoke (`/healthz`) and **CRUD** tests added; Makefile targets `smoke`, `crud-local`, `crud-prod`  
19. **Ephemeral E2E CI** — ✅ Postgres service → Alembic → API → k6 CRUD (manual trigger)

## Current step
* Project complete. Future items below are optional polish only.

## Test status
* Summary: **24 passed** locally (`pytest -q` on 2025-09-02); **24 passed** in CI.
* Coverage: ~90%+ (threshold enforced).
* Uptime workflow: latest scheduled/manual runs **passing** (Slack on failure).
* k6: smoke p95 < 800ms (prod); CRUD passes with `unexpected_error_rate==0`.

## Database & migrations
* Local DB: Postgres 16 @ localhost:5432  
* Render DB: Managed Postgres add-on (`DATABASE_URL`)  
* Alembic head: **73f82b54943b** (`add_entry_table`)  
* `alembic current`: ✅ matches head  
* Pending migrations: **0**  
* CI DB: GitHub Actions Postgres service (ephemeral workflow)

## Deployment notes
* `render.yaml`: converts `postgres://` → `postgresql+asyncpg://`; `LOG_LEVEL=INFO`; `PROMETHEUS_ENABLED=true`; `healthCheckPath: /healthz`; `postdeployCommand: alembic upgrade head`.
* App exposes `/metrics` when `PROMETHEUS_ENABLED=true`.

## Releases
* **v1.0.0** — first deployed version (Render)  
* **v1.0.1** — docs/state updates; Render blueprint & polish  
* **v1.0.2** — Ops & Monitoring: metrics + uptime (Slack) + k6 + ephemeral E2E

## Optional next ideas
* [ ] Sentry DSN + 2-line error triage note in README.  
* [ ] Light load/perf tests and SLOs.  
* [ ] Multi-cloud showcase (AWS App Runner/ECS) with IaC snippet.
