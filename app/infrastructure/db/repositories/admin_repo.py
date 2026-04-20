from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.admin.entity import Admin
from app.domain.admin.repository import AbstractAdminRepository
from app.infrastructure.db.models.admin_model import AdminModel


def _to_entity(m: AdminModel) -> Admin:
    return Admin(
        id=m.id,
        username=m.username,
        password_hash=m.password_hash,
        created_at=m.created_at,
    )


class AdminRepository(AbstractAdminRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_username(self, username: str) -> Optional[Admin]:
        result = await self._session.execute(
            select(AdminModel).where(AdminModel.username == username)
        )
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def get_by_id(self, admin_id: int) -> Optional[Admin]:
        m = await self._session.get(AdminModel, admin_id)
        return _to_entity(m) if m else None

    async def create(self, admin: Admin) -> Admin:
        m = AdminModel(
            username=admin.username,
            password_hash=admin.password_hash,
        )
        self._session.add(m)
        await self._session.flush()
        await self._session.refresh(m)
        return _to_entity(m)
