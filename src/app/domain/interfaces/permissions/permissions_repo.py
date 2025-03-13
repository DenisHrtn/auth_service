from abc import ABC, abstractmethod

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork


class PermissionsRepo(ABC):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    @abstractmethod
    async def get_permission_by_id(self, permission_id: int):
        pass

    @abstractmethod
    async def get_permissions(self):
        pass

    @abstractmethod
    async def update_permission(self, permission_model, **kwargs) -> str:
        pass
