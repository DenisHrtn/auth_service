from abc import ABC, abstractmethod

from app.domain.entities.role.dto import RoleCreatedDTO, RoleDTO


class CreateRoleUseCase(ABC):
    @abstractmethod
    def execute(self, dto: RoleCreatedDTO) -> RoleDTO:
        pass
