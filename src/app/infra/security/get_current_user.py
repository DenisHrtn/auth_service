from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jwt.exceptions import ExpiredSignatureError

from app.infra.security.decode_tokens import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Security(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

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
