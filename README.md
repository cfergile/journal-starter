Got you. Here’s a one-shot command that backs up your current README, writes the polished version (with a “How to Contribute” footer), and commits it.

````bash
# Backup, replace README.md, and commit
cp README.md README.md.bak-$(date +%F) 2>/dev/null || true

cat > README.md <<'MD'
# Journal API

[![CI](https://github.com/cfergile/journal-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/cfergile/journal-starter/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/cfergile/journal-starter/branch/main/graph/badge.svg)](https://codecov.io/gh/cfergile/journal-starter)
![Release](https://img.shields.io/github/v/release/cfergile/journal-starter?sort=semver)
[![Uptime - API Health](https://github.com/cfergile/journal-starter/actions/workflows/uptime.yml/badge.svg)](https://github.com/cfergile/journal-starter/actions/workflows/uptime.yml)
[![k6 CRUD (ephemeral env)](https://github.com/cfergile/journal-starter/actions/workflows/k6-crud-ephemeral.yml/badge.svg)](https://github.com/cfergile/journal-starter/actions/workflows/k6-crud-ephemeral.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


A FastAPI-based CRUD Journal API built as part of the **Learn to Cloud Guide** capstone project.  
Goal: practice Python, APIs, databases, testing — and ship it publicly.

---

## 🌐 Live Demo (Render)

- Base: **https://journal-starter.onrender.com**  
- Health: **/healthz** → https://journal-starter.onrender.com/healthz  
- Docs: **/docs** → https://journal-starter.onrender.com/docs

> Free tier note: cold starts can make the first request a bit slow.

---

## 🎯 Objectives

**Core (capstone):**
- FastAPI REST API
- CRUD for journal entries
- PostgreSQL + Alembic migrations
- pytest + httpx.AsyncClient tests

**Extended:**
- Docker & Makefile for reproducible dev
- CI quality gates (lint, type, security, coverage)
- Public deploy on Render (free)
- Ops & Monitoring (health, metrics, uptime + Slack, k6)

---

## 🚀 Features

- **POST** `/entries/` — create entry  
- **GET** `/entries/` — list entries  
- **GET** `/entries/{id}` — get entry  
- **PUT** `/entries/{id}` — update entry  
- **DELETE** `/entries/{id}` — delete entry  
- **GET** `/healthz` — health check  
- **GET** `/metrics` — Prometheus metrics (enabled when `PROMETHEUS_ENABLED=true`)

Entry fields: `work`, `struggle`, `intention`, plus `id`, `created_at`, `updated_at`.

---

## 🛠 Setup Options

### 1) Local (recommended for dev)

**Requirements:** Python 3.11+, local Postgres.

```bash
git clone https://github.com/cfergile/journal-starter.git
cd journal-starter

cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# DB migrate
alembic upgrade head

# Run API
uvicorn app.main:app --reload
# or: make run

# Local endpoints
# API:  http://localhost:8000
# Docs: http://localhost:8000/docs
````

### 2) Docker Compose

**Requirements:** Docker / Docker Compose.

```bash
git clone https://github.com/cfergile/journal-starter.git
cd journal-starter

cp .env.example .env
make compose-up
make compose-migrate  # runs Alembic upgrade in the container
```

---

## 🧪 Testing & CI Quality Gates

Local gates (mirror CI):

```bash
make precommit   # ruff, black, isort, mypy
make test        # pytest -q
make cov         # coverage in terminal
make ci          # coverage XML + threshold ≥90%
make lint-fix    # autofix linting
```

CI includes: Ruff • Black • isort • mypy • pytest • Bandit • Trivy FS (passing) • Codecov.

### k6 quick checks

```bash
# Smoke test against prod (hits /healthz)
make smoke
# Override to test locally:
make smoke BASE_URL=http://localhost:8000

# CRUD test against local dev (safe)
make crud-local

# (Opt-in) CRUD against prod (mutates prod data — only when you mean it)
make crud-prod
```

Ephemeral E2E (CI): the `k6-crud-ephemeral.yml` workflow spins up Postgres → runs Alembic → starts the API → runs the k6 CRUD test. Does **not** touch prod/staging.

---

## ⚙️ Environment Variables

See `.env.example` for the full list.

```ini
# Database (pieces)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=journal
DB_USER=postgres
DB_PASSWORD=change_this_password

# Optional full DSN for async SQLAlchemy (authoritative at runtime via settings.database_url)
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/journal

# Ops
LOG_LEVEL=INFO
# Enable Prometheus /metrics
PROMETHEUS_ENABLED=true
# Optional error tracking
# SENTRY_DSN=...
```

Alembic uses a sync URL for migrations, while the app uses the async DSN at runtime.
Render injects `DATABASE_URL`; the `render.yaml` converts it to `postgresql+asyncpg://` on start.

---

## 🛡️ Ops & Monitoring

* Healthcheck: `GET /healthz` → `{"status":"ok"}`
* Metrics: `GET /metrics` (enabled when `PROMETHEUS_ENABLED=true`)
* Logging: Python logging + Uvicorn access logs (`LOG_LEVEL=INFO` by default)
* Uptime: GitHub Actions cron (warm-up, retries, Slack alert on failure)
* Runtime: Inspect deploy history, logs, and health via Render dashboard

**Quick checks:**

```bash
# health
curl -fsS https://journal-starter.onrender.com/healthz || echo "DOWN"

# metrics (if enabled)
curl -fsS https://journal-starter.onrender.com/metrics | head
```

---

## 📦 Tech Stack

FastAPI • SQLAlchemy 2.0 (async) • Alembic • PostgreSQL • pytest/httpx
Ruff • Black • isort • mypy • Bandit • Trivy • GitHub Actions • Codecov
Render (deploy) • Prometheus-style metrics • k6

---

## 📚 Learning Outcomes

* Built and tested an async API with migrations
* Reproducible dev via Makefile/Docker
* Hardened CI (lint/type/security/coverage)
* Public deploy on Render with Postgres add-on
* Ops: health, metrics, uptime+Slack, smoke/CRUD performance checks

---

## ☁️ Deployment

✅ Render (live): [https://journal-starter.onrender.com](https://journal-starter.onrender.com)

---

## 🤝 How to Contribute

Contributions welcome!

1. **Fork & clone** this repo.
2. **Create a branch**: `git checkout -b feat/short-title`
3. **Set up locally** and run checks:

   ```bash
   make precommit
   make ci
   ```
4. **Add tests** for new behavior when possible.
5. **Commit** with a clear message (e.g., `feat: add XYZ` or `fix: handle ABC`).
6. **Push & open a PR** against `main`.
7. Ensure **CI is green** (lint, tests, security, coverage).

Thanks for helping make this project better!
MD

