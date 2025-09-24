from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entry import Entry as EntryModel
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate


class EntryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_entry(self, entry_in: EntryCreate) -> EntryOut:
        new_entry = EntryModel(
            id=str(uuid4()),
            work=entry_in.work,
            struggle=entry_in.struggle,
            intention=entry_in.intention,
        )
        self.db.add(new_entry)
        await self.db.commit()
        await self.db.refresh(new_entry)
        return EntryOut.model_validate(new_entry)

    async def get_entry_by_id(self, entry_id: str) -> EntryOut | None:
        result = await self.db.execute(select(EntryModel).where(EntryModel.id == entry_id))
        entry = result.scalar_one_or_none()
        return EntryOut.model_validate(entry) if entry else None

    async def get_all_entries(self) -> list[EntryOut]:
        result = await self.db.execute(select(EntryModel))
        entries = result.scalars().all()
        return [EntryOut.model_validate(entry) for entry in entries]

    async def update_entry(self, entry_id: str, entry_in: EntryUpdate) -> EntryOut | None:
        result = await self.db.execute(select(EntryModel).where(EntryModel.id == entry_id))
        entry = result.scalar_one_or_none()
        if not entry:
            return None
        for field, value in entry_in.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)
        await self.db.commit()
        await self.db.refresh(entry)
        return EntryOut.model_validate(entry)

    async def delete_entry(self, entry_id: str) -> bool:
        result = await self.db.execute(select(EntryModel).where(EntryModel.id == entry_id))
        entry = result.scalar_one_or_none()
        if not entry:
            return False
        await self.db.delete(entry)
        await self.db.commit()
        return True

# --- added by one-shot: flexible listing helper ---
from typing import Optional

# Note: local imports keep this patch self-contained
async def query_entries(
    session, *,
    limit: int = 50,
    offset: int = 0,
    q: Optional[str] = None,
    sort: str = "new",  # "new" | "old"
):
    from sqlalchemy import select, or_
    from app.models.entry import Entry

    stmt = select(Entry)

    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                Entry.work.ilike(pattern),
                Entry.struggle.ilike(pattern),
                Entry.intention.ilike(pattern),
            )
        )

    stmt = stmt.order_by(
        Entry.created_at.desc() if sort == "new" else Entry.created_at.asc()
    ).limit(limit).offset(offset)

    res = await session.execute(stmt)
    return list(res.scalars().all())
