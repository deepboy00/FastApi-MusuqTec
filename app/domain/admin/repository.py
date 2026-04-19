from abc import ABC, abstractmethod
from typing import Optional

from app.domain.admin.entity import Admin


class AbstractAdminRepository(ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Admin]:
        ...

    @abstractmethod
    async def get_by_id(self, admin_id: int) -> Optional[Admin]:
        ...

    @abstractmethod
    async def create(self, admin: Admin) -> Admin:
        ...
