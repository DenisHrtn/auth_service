import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

from app.application.interfaces.login.dto import (
    AuthTokenDTO,
    CreateJWTTokenDTO,
    VerifyPasswordDTO,
)
from app.application.interfaces.login.login_interface import ILoginInterface

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class LoginService(ILoginInterface):
    async def verify_password(self, dto: VerifyPasswordDTO):
        """
        Метод для проверки пароля
        """

        return pwd_context.verify(dto.plain_password, dto.hashed_password)

    async def hash_password(self, password: str) -> str:
        """
        Метод для хеширования пароля
        """

        return pwd_context.hash(password)

    async def create_jwt_token(self, dto: CreateJWTTokenDTO) -> str:
        """
        Функция для создания JWT-токена с указанным сроком жизни
        """

        to_encode = dto.data.copy()
        expire = datetime.now() + dto.expired_data
        to_encode.update({"exp": int(expire.timestamp())})

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def create_access_token(self, dto: AuthTokenDTO) -> str:
        """
        Функция для создания access token
        """

        token_dto = CreateJWTTokenDTO(
            data={
                "user_id": dto.user_id,
                "email": dto.email,
                "role_name": dto.role_name,
            },
            expired_data=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return await self.create_jwt_token(token_dto)

    async def create_refresh_token(self, dto: AuthTokenDTO) -> str:
        """
        Функция для создания  refresh token
        """

        token_dto = CreateJWTTokenDTO(
            data={
                "user_id": dto.user_id,
                "email": dto.email,
                "role_name": dto.role_name,
            },
            expired_data=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return await self.create_jwt_token(token_dto)
