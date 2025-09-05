# app/core/config.py
from __future__ import annotations

import os
from functools import lru_cache
from typing import ClassVar

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict  # Pydantic v2 settings


class Settings(BaseSettings):
    """
    Centralized application settings (Pydantic v2).
    - Prefers DATABASE_URL when present; otherwise builds async URL from DB_* pieces.
    - Exposes a .sync_database_url for Alembic (strips +asyncpg).
    - Adds Ops/Monitoring toggles used by app.main:
        LOG_LEVEL, PROMETHEUS_ENABLED, SENTRY_DSN, DEV_BIND_ALL
    """

    # ---------------------- Database (pieces) ----------------------
    db_host: str = Field(default="localhost", validation_alias=AliasChoices("DB_HOST", "db_host"))
    db_port: int = Field(default=5432, validation_alias=AliasChoices("DB_PORT", "db_port"))
    db_name: str = Field(default="journal", validation_alias=AliasChoices("DB_NAME", "db_name"))
    db_user: str = Field(default="postgres", validation_alias=AliasChoices("DB_USER", "db_user"))
    db_password: str = Field(
        default="postgres", validation_alias=AliasChoices("DB_PASSWORD", "db_password")
    )

    # Full DSN override (authoritative if provided)
    DATABASE_URL: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )

    # ---------------------- Ops & Monitoring ----------------------
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("LOG_LEVEL", "log_level"))
    prometheus_enabled: bool = Field(
        default=True, validation_alias=AliasChoices("PROMETHEUS_ENABLED", "prometheus_enabled")
    )
    sentry_dsn: str | None = Field(
        default=None, validation_alias=AliasChoices("SENTRY_DSN", "sentry_dsn")
    )
    dev_bind_all: bool = Field(
        default=False, validation_alias=AliasChoices("DEV_BIND_ALL", "dev_bind_all")
    )

    # Allowed levels (class-level constant for validation)
    _ALLOWED_LEVELS: ClassVar[set[str]] = {
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET",
    }

    # Pydantic v2 settings config:
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # tolerate unrelated keys (avoids Alembic crashes)
        env_prefix="",  # read variables as-is
    )

    # Normalize/validate log level
    @field_validator("log_level", mode="before")
    @classmethod
    def _normalize_log_level(cls, v: str) -> str:
        if v is None:
            return "INFO"
        level = str(v).upper().strip()
        return level if level in cls._ALLOWED_LEVELS else "INFO"

    # ---------------------- Derived URLs ----------------------
    @property
    def database_url(self) -> str:
        """
        Single source of truth for the app’s async DB URL.
        Precedence:
          1) env var DATABASE_URL / database_url (via Pydantic or os.environ)
          2) piecewise settings (db_user/password/host/port/name)
        Normalizes to 'postgresql+asyncpg://...' for the async engine.
        """
        # Prefer what Pydantic loaded, but also look directly at the environment
        url = os.getenv("DATABASE_URL") or os.getenv("database_url") or self.DATABASE_URL
        if url:
            # Normalize to async driver if needed
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url

        # Fallback from parts (async driver)
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sync_database_url(self) -> str:
        """
        Convenience for Alembic or other sync-only tools.
        Converts '+asyncpg' to sync psycopg/psycopg2-style URL.
        """
        return self.database_url.replace("postgresql+asyncpg://", "postgresql://", 1)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
