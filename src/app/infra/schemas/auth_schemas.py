from pydantic import BaseModel


class RegisterRequestSchema(BaseModel):
    email: str
    username: str
    password: str


class ConfirmRegistrationRequestSchema(BaseModel):
    email: str
    code: int


class SendCodeAgainRequestSchema(BaseModel):
    email: str


class LoginRequestSchema(BaseModel):
    email: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
