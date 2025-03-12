import logging
import os
import time

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status

from app.application.interfaces.decode_token.decode_tokens import IDecodeJWTToken

loger = logging.getLogger(__name__)

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class DecodeJWTToken(IDecodeJWTToken):
    async def decode_jwt_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp_time = payload.get("exp")
            current_time = int(time.time())

            loger.info(
                f"exp в токене: {exp_time}, текущее Unix-время сервера: {current_time}"
            )

            return payload
        except jwt.ExpiredSignatureError:
            loger.error("Ошибка: Токен истёк!")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
            )
        except jwt.InvalidTokenError as e:
            loger.error(f"Ошибка: Невалидный токен! {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен"
            )

    async def check_is_admin(self, token: str):
        payload = await self.decode_jwt_token(token)

        role_name = payload["role_name"]

        if role_name == "admin":
            return role_name

        return role_name
