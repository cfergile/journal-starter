Here’s a complete, copy-paste ready **`CONTRIBUTING.md`** you can drop into your repo.

````markdown
# Contributing

Thanks for helping improve **Journal API**! This repo is a small FastAPI + PostgreSQL CRUD service with tests, migrations, and k6 scripts. PRs that keep things simple, well-tested, and well-documented are 💯.

---

## Quick Start

1. **Fork & clone**
   ```bash
   git clone https://github.com/<you>/journal-starter.git
   cd journal-starter
````

2. **Python venv & deps**

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   # optional dev tools:
   pip install -r dev-requirements.txt
   ```

3. **Environment**

   ```bash
   cp .env.example .env
   # defaults assume local Postgres on :5432 with user/password postgres/postgres
   ```

4. **Database migrations**

   ```bash
   alembic upgrade head
   ```

5. **Run the API**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   # Docs: http://localhost:8000/docs
   ```

6. **Optional: Docker path**

   ```bash
   make compose-up
   make compose-migrate
   # API will be reachable per docker-compose mapping
   ```

7. **Sanity check (k6 CRUD, local)**

   ```bash
   BASE_URL=http://localhost:8000 k6 run k6/entries_crud.js
   ```

---

## Project Layout

```
app/
  core/        # settings/config
  db/          # session + base
  models/      # SQLAlchemy models
  schemas/     # Pydantic schemas
  services/    # business logic
  routers/     # FastAPI routers (entries)
migrations/    # Alembic env + versions
tests/         # unit + integration tests
k6/            # smoke + CRUD scripts
```

---

## Dev Workflow

* **Create a branch**

  ```bash
  git checkout -b feat/short-title
  ```
* Keep PRs focused. If behavior changes, **add/adjust tests**.
* Run the same quality gates locally that CI runs (below).

### Make targets (mirrors CI)

```bash
make precommit   # ruff, black, isort, mypy (+ quick k6 smoke/CRUD if configured)
make test        # pytest -q
make cov         # show coverage in terminal
make ci          # coverage xml + fail if <90%
make lint-fix    # auto-fix linting where safe

# Helpful extras
make run                 # uvicorn dev run (if defined)
make compose-up          # docker compose up
make compose-migrate     # alembic upgrade inside container
make smoke               # k6 smoke (defaults to prod unless BASE_URL is set)
make crud-local          # k6 full CRUD vs localhost
```

> Tip: For `make smoke` against local, explicitly set:
>
> ```bash
> make smoke BASE_URL=http://localhost:8000
> ```

---

## Tests

* We use **pytest**; async tests via **httpx.AsyncClient** and anyio.
* Minimum **coverage: 90%** (CI fails if lower).
* Integration tests expect a running DB and migrated schema (`alembic upgrade head`).

Run them:

```bash
make test
# or with coverage gates
make ci
```

---

## Database & Migrations

* Edit models in `app/models/` and keep schema changes small.
* Create a new migration:

  ```bash
  alembic revision -m "explain the change"
  # edit the generated script if needed
  alembic upgrade head
  ```
* Do **not** manually edit existing, committed migrations (create new ones).

---

## Style & Type Checks

* **Ruff** (lint), **Black** (format), **isort** (imports), **mypy** (types).
* Config lives in `pyproject.toml`, `ruff.toml`, `mypy.ini`, etc.
* Run:

  ```bash
  make precommit
  make lint-fix
  ```

---

## Commits & PRs

* Prefer **Conventional Commits**:

  * `feat: add entry soft-delete`
  * `fix: handle 404 on get by id`
  * `docs: update README badges`
  * `chore: bump deps`
  * `test: cover service error path`
* **PR checklist**

  * [ ] CI is green (`make ci`)
  * [ ] Tests added/updated
  * [ ] Migrations included (if schema changed)
  * [ ] Docs updated (README/STATE.md) if behavior/config changed
  * [ ] No secrets committed (`.env` is gitignored)

---

## k6 Notes

* **Local CRUD** (safe):

  ```bash
  BASE_URL=http://localhost:8000 k6 run k6/entries_crud.js
  ```
* **Prod CRUD** mutates live data — only run if you *really* mean it.

---

## Environment

Minimal `.env` (see `.env.example` for full):

```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=journal
DB_USER=postgres
DB_PASSWORD=postgres
# Or: DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/journal

LOG_LEVEL=INFO
PROMETHEUS_ENABLED=true
```

---

## Security & Responsible Disclosure

If you find a security issue, please open a minimal issue without sensitive details and we’ll coordinate privately. Avoid posting secrets or tokens in logs or PRs.

---

## License & Contributions

This project is licensed under the MIT License (see [LICENSE](LICENSE)).

By submitting a pull request, you agree that your contributions will be
licensed under the terms of the MIT License for this repository.


Thanks again for contributing! 🙌

```
::contentReference[oaicite:0]{index=0}
```
