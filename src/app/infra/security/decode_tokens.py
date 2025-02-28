import os
import time

import jwt
from fastapi import HTTPException, status

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def decode_jwt_token(token: str):
    """
    Функция для декодирования токена
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = payload.get("exp")
        current_time = int(time.time())

        print(f"exp в токене: {exp_time}, текущее Unix-время сервера: {current_time}")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен"
        )
