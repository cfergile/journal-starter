from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError  # NEW: for DB error cases

from app.models.entry import Entry as EntryModel
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate
from app.services.entry_service import EntryService


# -- Helper for all tests: always provide valid UTC datetimes
def fake_entry_model(**overrides):
    now = datetime.now(UTC)
    defaults = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "work": "Did some cloud learning",
        "struggle": "Struggled with SQL joins",
        "intention": "Practice joins tomorrow",
        "created_at": now,
        "updated_at": now,
    }
    defaults.update(overrides)
    return EntryModel(**defaults)


@pytest.fixture
def fake_db():
    db = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.fixture
def service(fake_db):
    return EntryService(db=fake_db)


@pytest.mark.anyio
async def test_get_entry_by_id_found(service, fake_db):
    entry = fake_entry_model()
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = entry
    fake_db.execute.return_value = result_mock

    result = await service.get_entry_by_id(entry.id)
    assert isinstance(result, EntryOut)
    assert str(result.id) == str(entry.id)
    assert result.work == entry.work


@pytest.mark.anyio
async def test_create_entry(service, fake_db):
    create_schema = EntryCreate(
        work="Write a test for create_entry",
        struggle="Mocking session methods",
        intention="Ensure entry gets created",
    )
    now = datetime.now(UTC)

    # Patch refresh to set created_at/updated_at after "DB commit"
    async def fake_refresh(entry):
        entry.created_at = now
        entry.updated_at = now

    fake_db.refresh.side_effect = fake_refresh

    result = await service.create_entry(create_schema)
    assert isinstance(result, EntryOut)
    assert result.work == create_schema.work
    assert result.created_at == now
    assert result.updated_at == now


@pytest.mark.anyio
async def test_update_entry_found(service, fake_db):
    entry = fake_entry_model()
    updated = fake_entry_model(work="Updated work")
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = entry
    fake_db.execute.return_value = result_mock
    fake_db.commit.return_value = None
    fake_db.refresh.return_value = None

    # Patch get_entry_by_id to simulate the updated entry after refresh
    service.get_entry_by_id = AsyncMock(return_value=EntryOut.model_validate(updated))

    update_schema = EntryUpdate(work="Updated work")
    result = await service.update_entry(entry.id, update_schema)
    assert isinstance(result, EntryOut)
    assert result.work == "Updated work"


@pytest.mark.anyio
async def test_update_entry_not_found(service, fake_db):
    # Simulate no entry found
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    fake_db.execute.return_value = result_mock

    update_schema = EntryUpdate(work="Will not be found")
    result = await service.update_entry("non-existent-id", update_schema)
    assert result is None


@pytest.mark.anyio
async def test_delete_entry_found(service, fake_db):
    entry = fake_entry_model()
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = entry
    fake_db.execute.return_value = result_mock
    fake_db.commit.return_value = None

    result = await service.delete_entry(entry.id)
    assert result is True


@pytest.mark.anyio
async def test_delete_entry_not_found(service, fake_db):
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    fake_db.execute.return_value = result_mock

    result = await service.delete_entry("non-existent-id")
    assert result is False


@pytest.mark.anyio
async def test_get_all_entries(service, fake_db):
    entries = [fake_entry_model(), fake_entry_model(id=str(uuid4()))]
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = entries
    fake_db.execute.return_value = result_mock

    result = await service.get_all_entries()
    assert isinstance(result, list)
    assert len(result) == 2
    for entry in result:
        assert isinstance(entry, EntryOut)


# ---------------------------
# New edge-case tests appended
# ---------------------------


@pytest.mark.anyio
async def test_get_all_entries_empty_list(service, fake_db):
    """Service should return an empty list when no rows are found."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = []
    fake_db.execute.return_value = result_mock

    result = await service.get_all_entries()
    assert result == []


@pytest.mark.anyio
async def test_create_entry_db_error_propagates(service, fake_db):
    """If the DB commit raises, the exception should surface (or adjust if caught)."""
    create_schema = EntryCreate(work="x", struggle="y", intention="z")
    fake_db.commit.side_effect = SQLAlchemyError("boom")

    with pytest.raises(SQLAlchemyError):
        await service.create_entry(create_schema)


@pytest.mark.anyio
async def test_update_entry_db_error_propagates(service, fake_db):
    """Update path: found row but commit fails -> exception surfaces (or adjust if caught)."""
    now = datetime.now(UTC)
    existing = EntryModel(
        id="123e4567-e89b-12d3-a456-426614174000",
        work="w",
        struggle="s",
        intention="i",
        created_at=now,
        updated_at=now,
    )
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = existing
    fake_db.execute.return_value = result_mock

    fake_db.commit.side_effect = SQLAlchemyError("fail")
    update_schema = EntryUpdate(work="new")

    with pytest.raises(SQLAlchemyError):
        await service.update_entry(existing.id, update_schema)
