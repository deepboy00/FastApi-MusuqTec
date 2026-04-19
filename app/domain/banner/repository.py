from abc import ABC, abstractmethod
from typing import Optional

from app.domain.banner.entity import Banner


class AbstractBannerRepository(ABC):

    @abstractmethod
    async def get_all(self, activo_only: bool = True) -> list[Banner]:
        ...

    @abstractmethod
    async def get_by_id(self, banner_id: int) -> Optional[Banner]:
        ...

    @abstractmethod
    async def create(self, banner: Banner) -> Banner:
        ...

    @abstractmethod
    async def update(self, banner: Banner) -> Banner:
        ...

    @abstractmethod
    async def delete(self, banner_id: int) -> None:
        ...
