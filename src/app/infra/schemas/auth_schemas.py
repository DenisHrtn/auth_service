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


class ResetPasswordSchema(BaseModel):
    email: str


class ChangePasswordSchema(BaseModel):
    code: int
    password: str
    password_again: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
