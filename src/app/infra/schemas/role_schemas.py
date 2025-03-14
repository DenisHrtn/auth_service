from pydantic import BaseModel


class UpdateRoleSchema(BaseModel):
    role_name: str
    description: str
    permissions: list[int]
