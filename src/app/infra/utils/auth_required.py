from functools import wraps

import redis
from fastapi import HTTPException, Request

from app.containers import container
from app.infra.services.jwt_auth_service import JWTAuthService

jwt_auth = JWTAuthService(redis_cl=redis.Redis)


def auth_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = await get_token(request)
        print(f"Token received in wrapper: {token} (type: {type(token)})")

        auth_service = container.auth.auth_service()
        await auth_service.validate_token(token)

        return await func(request, *args, **kwargs)

    return wrapper


async def get_token(request: Request):
    token = request.headers.get("Authorization")
    print(f"Received Authorization header: {token}")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    extracted_token = token.split(" ")[1]
    print(f"Extracted token: {extracted_token}")

    return extracted_token
