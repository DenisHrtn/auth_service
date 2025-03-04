from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jwt.exceptions import ExpiredSignatureError

from app.containers import container
from app.infra.security.decode_tokens import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    redis_client=Depends(lambda: container.redis.redis_client()),
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not redis_client.exists(f"token:{token}"):
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

    try:
        payload = decode_jwt_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
