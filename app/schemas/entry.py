from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# Base schema for shared fields
class EntryBase(BaseModel):
    work: str = Field(..., max_length=256, description="What did you work on today?")
    struggle: str = Field(
        ..., max_length=256, description="What’s one thing you struggled with today?"
    )
    intention: str = Field(..., max_length=256, description="What will you study/work on tomorrow?")


# Used for entry creation (POST)
class EntryCreate(EntryBase):
    pass


# Used for entry update (PUT/PATCH) - allow partial updates
class EntryUpdate(BaseModel):
    work: str | None = None
    struggle: str | None = None
    intention: str | None = None

    model_config = ConfigDict(extra="forbid")  # Disallow unknown fields


# Used for reading from DB and returning to client
class EntryOut(EntryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
