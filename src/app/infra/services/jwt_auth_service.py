import logging
import os
from datetime import timedelta
from typing import Optional

import jwt
import redis.asyncio as redis
from dotenv import load_dotenv
from fastapi import HTTPException

from app.domain.interfaces.auth.auth_interface import IAuthInterface

logger = logging.getLogger(__name__)

load_dotenv()

AUTH_SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES", 60))

redis_client = redis.Redis(
    host=os.getenv("REDIS_CONFIG__host"),
    port=int(os.getenv("REDIS_PORT__port")),
    decode_responses=True,
)


class JWTAuthService(IAuthInterface):
    def __init__(self, redis_cl: redis.Redis) -> None:
        self.redis_cl = redis_cl

    async def put_token_in_redis(self, token: str) -> str:
        expiry_time = timedelta(minutes=TOKEN_EXPIRY_MINUTES).total_seconds()

        result = self.redis_cl.setex(f"token:{token}", int(expiry_time), "active")

        return f"Токен успешно записан в Redis! {result}"

    async def validate_token(self, token: bytes) -> Optional[dict]:
        try:
            payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
            logger.info(f"Decoded payload: {payload}")
        except jwt.ExpiredSignatureError:
            self.deactivate_token(str(token))
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if not self.redis_cl.exists(f"token:{token}"):
            logger.warning("Token not found in Redis")
            raise HTTPException(status_code=401, detail="Invalid token")

        key = f"token:{token}"
        ttl = self.redis_cl.ttl(key)

        if ttl == -2:
            return {"detail": "Token expired"}
        if ttl > 0:
            status = self.redis_cl.get(key)
            return status

        return payload

    async def deactivate_token(self, token: str) -> None:
        await self.redis_cl.delete(f"token:{token}")
        logger.info(f"Токен {token} был успешно удален из Redis!")
