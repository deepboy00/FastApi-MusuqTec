from abc import ABC, abstractmethod
from typing import Optional

from app.domain.producto.entity import Producto


class AbstractProductoRepository(ABC):

    @abstractmethod
    async def get_all(self, activo_only: bool = True) -> list[Producto]:
        ...

    @abstractmethod
    async def get_by_id(self, producto_id: int) -> Optional[Producto]:
        ...

    @abstractmethod
    async def get_by_categoria(self, categoria_id: int) -> list[Producto]:
        ...

    @abstractmethod
    async def create(self, producto: Producto) -> Producto:
        ...

    @abstractmethod
    async def update(self, producto: Producto) -> Producto:
        ...

    @abstractmethod
    async def delete(self, producto_id: int) -> None:
        ...

    @abstractmethod
    async def decrement_stock(self, producto_id: int, cantidad: int = 1) -> Producto:
        ...
