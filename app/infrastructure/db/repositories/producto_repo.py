from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.producto.entity import Producto
from app.domain.producto.repository import AbstractProductoRepository
from app.infrastructure.db.models.producto_model import ProductoModel


def _to_entity(m: ProductoModel) -> Producto:
    from app.domain.producto.entity import ProductoSpec
    return Producto(
        id=m.id,
        nombre=m.nombre,
        slug=m.slug,
        tagline=m.tagline,
        descripcion=m.descripcion,
        precio=float(m.precio),
        stock=m.stock,
        sku=m.sku,
        categoria_id=m.categoria_id,
        imagen_url=m.imagen_url,
        imagen_thumb=m.imagen_thumb,
        activo=m.activo,
        vistas=m.vistas,
        wsp_clicks=m.wsp_clicks,
        specs=[ProductoSpec(id=s.id, spec=s.spec, orden=s.orden) for s in (m.specs or [])],
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


class ProductoRepository(AbstractProductoRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, activo_only: bool = True) -> list[Producto]:
        stmt = select(ProductoModel).order_by(ProductoModel.nombre)
        if activo_only:
            stmt = stmt.where(ProductoModel.activo.is_(True))
        result = await self._session.execute(stmt)
        return [_to_entity(r) for r in result.scalars().all()]

    async def get_by_id(self, producto_id: int) -> Optional[Producto]:
        m = await self._session.get(ProductoModel, producto_id)
        return _to_entity(m) if m else None

    async def get_by_categoria(self, categoria_id: int) -> list[Producto]:
        result = await self._session.execute(
            select(ProductoModel)
            .where(ProductoModel.categoria_id == categoria_id, ProductoModel.activo.is_(True))
            .order_by(ProductoModel.nombre)
        )
        return [_to_entity(r) for r in result.scalars().all()]

    async def create(self, producto: Producto) -> Producto:
        m = ProductoModel(
            nombre=producto.nombre,
            slug=producto.slug,
            tagline=producto.tagline,
            descripcion=producto.descripcion,
            precio=producto.precio,
            stock=producto.stock,
            sku=producto.sku,
            categoria_id=producto.categoria_id,
            imagen_url=producto.imagen_url,
            imagen_thumb=producto.imagen_thumb,
            activo=producto.activo,
            vistas=0,
            wsp_clicks=0,
        )
        self._session.add(m)
        await self._session.flush()
        await self._session.refresh(m)
        return _to_entity(m)

    async def update(self, producto: Producto) -> Producto:
        m = await self._session.get(ProductoModel, producto.id)
        if not m:
            raise ValueError(f"Producto {producto.id} no existe")
        m.nombre = producto.nombre
        m.slug = producto.slug
        m.tagline = producto.tagline
        m.descripcion = producto.descripcion
        m.precio = producto.precio
        m.stock = producto.stock
        m.sku = producto.sku
        m.categoria_id = producto.categoria_id
        m.imagen_url = producto.imagen_url
        m.imagen_thumb = producto.imagen_thumb
        m.activo = producto.activo
        await self._session.flush()
        return _to_entity(m)

    async def delete(self, producto_id: int) -> None:
        m = await self._session.get(ProductoModel, producto_id)
        if m:
            await self._session.delete(m)
            await self._session.flush()

    async def decrement_stock(self, producto_id: int, cantidad: int = 1) -> Producto:
        m = await self._session.get(ProductoModel, producto_id)
        if not m:
            raise ValueError(f"Producto {producto_id} no existe")
        if m.stock < cantidad:
            raise ValueError(f"Stock insuficiente (disponible: {m.stock})")
        m.stock -= cantidad
        await self._session.flush()
        return _to_entity(m)
