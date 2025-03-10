import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_jwt_token(data: dict, expired_data: timedelta) -> str:
    """
    Функция для создания JWT-токена с указанным сроком жизни
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + expired_data
    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int, email: str, role_name: str) -> str:
    """
    Функция для создания access token
    """

    return create_jwt_token(
        {"user_id": user_id, "email": email, "role_name": role_name},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: int, email: str, role_name: str):
    """
    Функция для создания  refresh token
    """
    return create_jwt_token(
        {"user_id": user_id, "email": email, "role_name": role_name},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
