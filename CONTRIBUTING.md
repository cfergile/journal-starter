# Contributing

Thanks for helping improve **Journal API**!

## Quick Start

1. Fork & clone your fork.
2. Create a virtualenv and install deps:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   # (optional) dev tools:
   pip install -r dev-requirements.txt
   ```
3. Copy env and run DB migrations (local Postgres on :5432):
   ```bash
   cp .env.example .env
   alembic upgrade head
   ```
4. Run the API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   # Docs -> http://localhost:8000/docs
   ```
   *(Docker users: `make compose-up && make compose-migrate`)*

## Dev Workflow

- Create a branch:
  ```bash
  git checkout -b feat/short-title
  ```
- Keep changes small and focused. Include tests where it makes sense.

### Quality Gates (mirror CI)

```bash
make precommit   # ruff, black, isort, mypy (+ quick k6 CRUD)
make test        # pytest -q
make cov         # coverage in terminal
make ci          # coverage XML + threshold ≥90%
make lint-fix    # autofix lint issues
```

### CRUD smoke locally

```bash
uvicorn app.main:app --reload &
BASE_URL=http://localhost:8000 k6 run k6/entries_crud.js
```

## Code Style

- **Python**: Ruff, Black, isort, mypy (configured in repo).
- **Structure**: `app/services` (business), `app/routers` (HTTP), `app/models` (ORM), `app/schemas` (Pydantic).

## Commits & PRs

- Prefer **Conventional Commits** (`feat:`, `fix:`, `docs:` …).
- PR checklist:
  - [ ] CI green (`make ci` locally)
  - [ ] Tests updated when behavior changes
  - [ ] Docs updated if needed
  - [ ] No secrets committed (`.env` is ignored)

## Issues & Security

- Bugs: repro steps, expected vs actual, minimal logs.
- Security: report minimal details; we’ll coordinate privately.

## License / Usage

If a LICENSE exists, contributions are accepted under that license. If not, usage defaults to “all rights reserved” by the maintainer.
