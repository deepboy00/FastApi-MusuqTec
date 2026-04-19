from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.admin.entity import Admin
from app.domain.admin.repository import AbstractAdminRepository
from app.infrastructure.db.models.admin_model import AdminModel


def _to_entity(m: AdminModel) -> Admin:
    return Admin(
        id=m.id,
        email=m.email,
        hashed_password=m.hashed_password,
        nombre=m.nombre,
        activo=m.activo,
    )


class AdminRepository(AbstractAdminRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> Optional[Admin]:
        result = await self._session.execute(
            select(AdminModel).where(AdminModel.email == email)
        )
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def get_by_id(self, admin_id: int) -> Optional[Admin]:
        m = await self._session.get(AdminModel, admin_id)
        return _to_entity(m) if m else None

    async def create(self, admin: Admin) -> Admin:
        m = AdminModel(
            email=admin.email,
            hashed_password=admin.hashed_password,
            nombre=admin.nombre,
            activo=admin.activo,
        )
        self._session.add(m)
        await self._session.flush()
        await self._session.refresh(m)
        return _to_entity(m)
