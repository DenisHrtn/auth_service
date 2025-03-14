from pydantic import BaseModel


class UpdatePermissionsRequest(BaseModel):
    description: str
