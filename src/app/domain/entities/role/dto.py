from dataclasses import dataclass


@dataclass
class RoleDTO:
    id: int
    role_name: str
    description: str
    permissions: list[int]
    user_id: int
