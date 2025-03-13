from abc import ABC, abstractmethod

from app.domain.entities.permission.dto import UpdatePermissionDto


class UpdatePermissionUseCase(ABC):
    @abstractmethod
    async def execute(self, permission_id: int, token: str, dto: UpdatePermissionDto):
        pass
