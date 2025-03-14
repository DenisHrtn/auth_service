from dataclasses import dataclass
from datetime import timedelta


@dataclass
class VerifyPasswordDTO:
    plain_password: str
    hashed_password: str


@dataclass
class CreateJWTTokenDTO:
    data: dict
    expired_data: timedelta


@dataclass
class AuthTokenDTO:
    user_id: int
    email: str
    role_name: str
