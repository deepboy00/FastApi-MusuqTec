from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.producto.entity import ProductoSpec
from app.infrastructure.db.models.producto_spec_model import ProductoSpecModel


def _to_entity(m: ProductoSpecModel) -> ProductoSpec:
    return ProductoSpec(id=m.id, spec=m.spec, orden=m.orden)


class ProductoSpecRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_producto(self, producto_id: int) -> list[ProductoSpec]:
        result = await self._session.execute(
            select(ProductoSpecModel)
            .where(ProductoSpecModel.producto_id == producto_id)
            .order_by(ProductoSpecModel.orden)
        )
        return [_to_entity(r) for r in result.scalars().all()]

    async def replace_all(self, producto_id: int, specs: list[ProductoSpec]) -> list[ProductoSpec]:
        """Elimina todas las specs del producto y las reemplaza."""
        existing = await self._session.execute(
            select(ProductoSpecModel).where(ProductoSpecModel.producto_id == producto_id)
        )
        for m in existing.scalars().all():
            await self._session.delete(m)

        nuevas = []
        for s in specs:
            m = ProductoSpecModel(producto_id=producto_id, spec=s.spec, orden=s.orden)
            self._session.add(m)
            nuevas.append(m)

        await self._session.flush()
        for m in nuevas:
            await self._session.refresh(m)

        return [_to_entity(m) for m in nuevas]
