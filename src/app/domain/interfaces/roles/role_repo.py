from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.role.dto import RoleCreatedDTO, RoleDTO
from app.domain.entities.role.entity import Role


class RoleRepo(ABC):
    @abstractmethod
    def create(self, dto: RoleCreatedDTO) -> RoleDTO:
        pass

    @abstractmethod
    def get_by_name(self, role_name: str) -> Optional[Role]:
        pass

    @abstractmethod
    def update_role(self, role_id: int, role: RoleDTO) -> RoleDTO:
        pass

    @abstractmethod
    def check_user_role(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete_role(self, role_id: int) -> None:
        pass
