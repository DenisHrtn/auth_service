from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.role.dto import RoleResponseDTO


@dataclass
class UserDTO:
    id: int
    email: str
    username: str
    hashed_password: str
    code: int
    code_created_at: datetime
    is_admin: bool
    is_active: bool
    is_blocked: bool
    date_joined: datetime


@dataclass
class UserResponseDTO:
    email: str
    username: str
    is_admin: bool
    is_active: bool
    is_blocked: bool
    date_joined: datetime


@dataclass
class AllUsersResponseDTO:
    id: int
    email: str
    username: str
    is_admin: bool
    is_active: bool
    is_blocked: bool
    date_joined: datetime
    role: RoleResponseDTO


@dataclass
class RegisterUserDTO:
    email: str
    username: str
    password: str


def map_user_to_dto(user):
    return AllUsersResponseDTO(
        id=user.id,
        email=user.email,
        username=user.username,
        is_admin=user.is_admin,
        is_active=user.is_active,
        is_blocked=user.is_blocked,
        date_joined=user.date_joined.isoformat(),
        role=RoleResponseDTO(
            id=user.role.id,
            role_name=user.role.role_name,
            description=user.role.description,
            permissions=user.role.permissions,
        ),
    )
