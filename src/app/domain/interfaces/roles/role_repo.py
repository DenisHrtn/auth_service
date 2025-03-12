from abc import ABC, abstractmethod
from typing import List, Optional

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.domain.entities.role.entity import Role


class RoleRepo(ABC):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    @abstractmethod
    async def get_by_name(self, role_name: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def update_role(self, role_model, **kwargs) -> str:
        pass

    @abstractmethod
    def check_user_role(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_roles(self) -> List[Role]:
        pass
