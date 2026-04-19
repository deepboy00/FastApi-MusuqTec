from abc import ABC, abstractmethod
from typing import Optional

from app.domain.categoria.entity import Categoria


class AbstractCategoriaRepository(ABC):

    @abstractmethod
    async def get_all(self) -> list[Categoria]:
        ...

    @abstractmethod
    async def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Categoria]:
        ...

    @abstractmethod
    async def create(self, categoria: Categoria) -> Categoria:
        ...

    @abstractmethod
    async def update(self, categoria: Categoria) -> Categoria:
        ...

    @abstractmethod
    async def delete(self, categoria_id: int) -> None:
        ...
