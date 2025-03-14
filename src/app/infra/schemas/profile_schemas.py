from pydantic import BaseModel


class UpdateProfileSchema(BaseModel):
    first_name: str
    last_name: str
    info: str
    speciality: str
