from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.categoria.entity import Categoria
from app.domain.categoria.repository import AbstractCategoriaRepository
from app.infrastructure.db.models.categoria_model import CategoriaModel


def _to_entity(m: CategoriaModel) -> Categoria:
    return Categoria(id=m.id, nombre=m.nombre, slug=m.slug, activo=m.activo)


class CategoriaRepository(AbstractCategoriaRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> list[Categoria]:
        result = await self._session.execute(select(CategoriaModel).order_by(CategoriaModel.nombre))
        return [_to_entity(r) for r in result.scalars().all()]

    async def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        m = await self._session.get(CategoriaModel, categoria_id)
        return _to_entity(m) if m else None

    async def get_by_slug(self, slug: str) -> Optional[Categoria]:
        result = await self._session.execute(
            select(CategoriaModel).where(CategoriaModel.slug == slug)
        )
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def create(self, categoria: Categoria) -> Categoria:
        m = CategoriaModel(nombre=categoria.nombre, slug=categoria.slug, activo=categoria.activo)
        self._session.add(m)
        await self._session.flush()
        await self._session.refresh(m)
        return _to_entity(m)

    async def update(self, categoria: Categoria) -> Categoria:
        m = await self._session.get(CategoriaModel, categoria.id)
        if not m:
            raise ValueError(f"Categoria {categoria.id} no existe")
        m.nombre = categoria.nombre
        m.slug = categoria.slug
        m.activo = categoria.activo
        await self._session.flush()
        return _to_entity(m)

    async def delete(self, categoria_id: int) -> None:
        m = await self._session.get(CategoriaModel, categoria_id)
        if m:
            await self._session.delete(m)
            await self._session.flush()
