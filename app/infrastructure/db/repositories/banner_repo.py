from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.banner.entity import Banner
from app.domain.banner.repository import AbstractBannerRepository
from app.infrastructure.db.models.banner_model import BannerModel


def _to_entity(m: BannerModel) -> Banner:
    return Banner(
        id=m.id,
        titulo=m.titulo,
        subtitulo=m.subtitulo,
        imagen_url=m.imagen_url,
        orden=m.orden,
        activo=m.activo,
        link=m.link,
    )


class BannerRepository(AbstractBannerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, activo_only: bool = True) -> list[Banner]:
        stmt = select(BannerModel).order_by(BannerModel.orden)
        if activo_only:
            stmt = stmt.where(BannerModel.activo.is_(True))
        result = await self._session.execute(stmt)
        return [_to_entity(r) for r in result.scalars().all()]

    async def get_by_id(self, banner_id: int) -> Optional[Banner]:
        m = await self._session.get(BannerModel, banner_id)
        return _to_entity(m) if m else None

    async def create(self, banner: Banner) -> Banner:
        m = BannerModel(
            titulo=banner.titulo,
            subtitulo=banner.subtitulo,
            imagen_url=banner.imagen_url,
            orden=banner.orden,
            activo=banner.activo,
            link=banner.link,
        )
        self._session.add(m)
        await self._session.flush()
        await self._session.refresh(m)
        return _to_entity(m)

    async def update(self, banner: Banner) -> Banner:
        m = await self._session.get(BannerModel, banner.id)
        if not m:
            raise ValueError(f"Banner {banner.id} no existe")
        m.titulo = banner.titulo
        m.subtitulo = banner.subtitulo
        m.imagen_url = banner.imagen_url
        m.orden = banner.orden
        m.activo = banner.activo
        m.link = banner.link
        await self._session.flush()
        return _to_entity(m)

    async def delete(self, banner_id: int) -> None:
        m = await self._session.get(BannerModel, banner_id)
        if m:
            await self._session.delete(m)
            await self._session.flush()
