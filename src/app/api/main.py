import os

from fastapi import FastAPI

from app.api.auth import router as auth_router
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
