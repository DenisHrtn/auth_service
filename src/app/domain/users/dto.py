from datetime import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    class Config:
        from_attributes = True

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
