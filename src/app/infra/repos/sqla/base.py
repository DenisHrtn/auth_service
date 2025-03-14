from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.config import Config

config = Config()

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata
