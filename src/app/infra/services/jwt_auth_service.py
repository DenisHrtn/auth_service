import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
import redis
from dotenv import load_dotenv
from fastapi import HTTPException

from app.domain.interfaces.auth.auth_interface import IAuthInterface

load_dotenv()

AUTH_SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES", 60))

redis_client = redis.Redis(
    host=os.getenv("REDIS_CONFIG__host"),
    port=int(os.getenv("REDIS_PORT__port")),
    decode_responses=True,
)


class JWTAuthService(IAuthInterface):
    def __init__(self, redis_client: redis.Redis) -> None:
        self.secret_key = AUTH_SECRET_KEY
        self.expiry_minutes = TOKEN_EXPIRY_MINUTES
        self.redis_client = redis_client

    async def generate_token(
        self,
        user_id: int,
        role_name: str,
        email: str,
    ) -> bytes:
        payload = {
            "user_id": user_id,
            "role_name": role_name,
            "email": email,
            "exp": datetime.now() + timedelta(minutes=self.expiry_minutes),
        }

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")

        await self.redis_client.setex(
            f"token:{token}", timedelta(minutes=self.expiry_minutes), "active"
        )

        return token

    async def validate_token(self, token: bytes) -> Optional[dict]:
        print(f"Token before decoding: {token} (type: {type(token)})")

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            print(f"Decoded payload: {payload}")
        except jwt.ExpiredSignatureError:
            print("Token expired")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {e}")
            raise HTTPException(status_code=401, detail="evrevre token")

        # if not self.redis_client.exists(f'token:{token}'):
        #     print("Token not found in Redis")
        #     raise HTTPException(status_code=401, detail="Ivvre")

        return payload

    async def deactivate_token(self, token: str) -> None:
        await self.redis_client.delete(f"token:{token}")
