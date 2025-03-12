from abc import ABC, abstractmethod

from app.domain.entities.role.dto import RoleDTO


class UpdateRoleUseCase(ABC):
    @abstractmethod
    async def execute(self, role: RoleDTO) -> RoleDTO:
        pass
