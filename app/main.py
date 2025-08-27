# app/main.py
from __future__ import annotations

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.routers.journal_router import router as journal_router

# Ensure we at least have INFO logs if nothing else configures logging.
root_logger = logging.getLogger()
if not root_logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    FastAPI lifespan handler. Logs DB URLs on startup.
    Add any shutdown logic after the `yield`.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("DB URL in use (async): %s", settings.database_url)
    if hasattr(settings, "sync_database_url"):
        logger.info("DB URL in use (sync): %s", settings.sync_database_url)
    yield  # place shutdown logic here later if needed


app = FastAPI(title="Journal API", version="0.1.0", lifespan=lifespan)


@app.get("/healthz", tags=["Health"], summary="Healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


# API routes
app.include_router(journal_router)

if __name__ == "__main__":
    import uvicorn

    # Default to localhost in dev to avoid Bandit B104; allow opt-in to 0.0.0.0 via env.
    host = "127.0.0.1"
    if os.getenv("DEV_BIND_ALL") == "1":
        host = "0.0.0.0"  # nosec B104: dev-only opt-in
    uvicorn.run("app.main:app", host=host, port=8000, reload=True)
