from dataclasses import dataclass
from datetime import datetime


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
