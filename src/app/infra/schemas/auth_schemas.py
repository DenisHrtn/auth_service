from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str


class ConfirmRegistrationRequest(BaseModel):
    email: str
    code: int


class SendCodeAgainRequest(BaseModel):
    email: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
