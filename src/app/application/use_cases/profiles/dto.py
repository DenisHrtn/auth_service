from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.user.dto import UserResponseDTO


@dataclass
class UpdateProfileDTO:
    first_name: str
    last_name: str
    info: str
    speciality: str


@dataclass
class ProfileDTO:
    id: int
    first_name: str
    last_name: str
    info: str
    speciality: str
    days_with_service: datetime
    user_id: int
    user: Optional[UserResponseDTO]


def map_profile_to_dto(profile) -> ProfileDTO:
    return ProfileDTO(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        info=profile.info,
        speciality=profile.speciality,
        days_with_service=profile.days_with_service,
        user_id=profile.user_id,
        user=(
            UserResponseDTO(
                email=profile.user.email,
                username=profile.user.username,
                is_admin=profile.user.is_admin,
                is_blocked=profile.user.is_blocked,
                date_joined=profile.user.date_joined.isoformat(),
                is_active=profile.user.is_active,
            )
            if profile.user
            else None
        ),
    )
