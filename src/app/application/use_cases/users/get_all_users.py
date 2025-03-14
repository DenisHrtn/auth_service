from abc import ABC, abstractmethod
from typing import Optional


class GetAllUsersUseCase(ABC):
    @abstractmethod
    async def get_all_users(
        self,
        offset: int,
        limit: int,
        is_admin: Optional[bool] = None,
        order_by: Optional[str] = None,
    ) -> list:
        pass
