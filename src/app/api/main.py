import os

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.permissions import router as permissions_router
from app.api.profiles import router as profiles_router
from app.api.roles import router as roles_router
from app.api.users import router as users_router
from app.config import Config
from app.containers import container

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

config = Config()
container.config.override(config)

container.wire(modules=["app.api.auth"])

app = FastAPI()
app.container = container

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(roles_router, prefix="/api/v1/roles")
app.include_router(permissions_router, prefix="/api/v1/permissions")
app.include_router(profiles_router, prefix="/api/v1/profiles")
app.include_router(users_router, prefix="/api/v1/users")
