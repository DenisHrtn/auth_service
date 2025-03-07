import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

from app.infra.security.get_current_user import get_current_user

load_dotenv()

AUTH_SECRET_KEY = os.getenv("SECRET_KEY")


def decode_jwt_token(request: Request):
    """
    Функция для декодирования JWT-токена
    :param request: FastAPI Request
    :return: user_id, role_name, email
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Токен не найден или неверного формата",
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Срок действия токена истёк"
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Неверный токен"
        ) from exc

    return payload.get("user_id"), payload.get("role_name"), payload.get("email")


def is_admin(user: dict = Depends(get_current_user)):
    if user.get("role_name") != "admin":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Доступ запрещен")
    return user
