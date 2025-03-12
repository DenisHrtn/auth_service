from dataclasses import dataclass
from typing import Optional

from app.domain.entities.user.dto import UserResponseDTO


@dataclass
class RoleDTO:
    id: int
    role_name: str
    description: str
    permissions: list[int]
    user_id: int
    user: Optional[UserResponseDTO]


@dataclass
class UpdateRoleRTO:
    role_name: str
    description: str
    permissions: list[int]


def map_role_to_dto(role) -> RoleDTO:
    return RoleDTO(
        id=role.id,
        role_name=role.role_name,
        description=role.description,
        user_id=role.user_id,
        permissions=role.permissions,
        user=(
            UserResponseDTO(
                email=role.user.email,
                username=role.user.username,
                is_admin=role.user.is_admin,
                is_blocked=role.user.is_blocked,
                date_joined=role.user.date_joined.isoformat(),
                is_active=role.user.is_active,
            )
            if role.user
            else None
        ),
    )
