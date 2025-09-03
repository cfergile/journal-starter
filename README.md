# Journal API

[![CI](https://github.com/cfergile/journal-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/cfergile/journal-starter/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/cfergile/journal-starter/branch/main/graph/badge.svg)](https://codecov.io/gh/cfergile/journal-starter)

A FastAPI-based CRUD Journal API built as part of the **Learn to Cloud Guide** capstone project.  
Goal: practice Python, APIs, databases, testing — and ship it publicly.

---

## 🌐 Live Demo (Render)
- Base: **https://journal-starter.onrender.com**  
- Health: **/healthz** → https://journal-starter.onrender.com/healthz  
- Docs: **/docs** → https://journal-starter.onrender.com/docs

> Note: Free tier may cold-start; first request can be a bit slow.

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

---

## 🚀 Features

- **POST** `/entries/` — create entry  
- **GET** `/entries/` — list entries  
- **GET** `/entries/{id}` — get entry  
- **PUT** `/entries/{id}` — update entry  
- **DELETE** `/entries/{id}` — delete entry  
- **GET** `/healthz` — health check

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
API: http://localhost:8000
Docs: http://localhost:8000/docs

2) Docker Compose
Requirements: Docker / Docker Compose.

bash
Copy code
git clone https://github.com/cfergile/journal-starter.git
cd journal-starter

cp .env.example .env
make compose-up
make compose-migrate  # runs alembic upgrade head in the container
🧪 Testing & CI Quality Gates
Local gates (mirror CI):

bash
Copy code
make precommit   # ruff, black, isort, mypy
make test        # pytest -q
make cov         # coverage in terminal
make ci          # coverage XML + threshold ≥90%
make lint-fix    # autofix linting
CI includes: Ruff • Black • isort • mypy • pytest • Bandit • Trivy FS (passing) • Codecov.

⚙️ Environment Variables
See .env.example for full list.

ini
Copy code
# Database (pieces)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=journal
DB_USER=postgres
DB_PASSWORD=postgres

# Optional full DSN for async SQLAlchemy
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/journal
Render deploy uses a managed Postgres add-on and provides a connection string via environment; the app’s Alembic env is configured to use psycopg3 for migrations.

📦 Tech Stack
FastAPI • SQLAlchemy 2.0 (async) • Alembic • PostgreSQL • pytest/httpx
Ruff • Black • isort • mypy • Bandit • Trivy • GitHub Actions • Codecov
Render (deploy)

📚 Learning Outcomes
Built and tested a real async API with migrations

Reproducible dev via Makefile/Docker

Hardened CI (lint/type/security/coverage)

Public deploy on Render with Postgres add-on

☁️ Deployment
✅ Render (live): https://journal-starter.onrender.com

🔜 Optional: AWS (ECS/App Runner) as a multi-cloud showcase