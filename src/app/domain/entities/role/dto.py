from dataclasses import dataclass


@dataclass
class RoleDTO:
    id: int
    role_name: str
    description: str
    permissions: list[int]
    user_id: int


@dataclass
class RoleResponseDTO:
    id: int
    role_name: str
    description: str
    permissions: list[int]


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
    )
