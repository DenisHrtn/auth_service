from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.app.config import Config

config = Config()

metadata = MetaData(schema=config.DB_CONFIG.schema_name)


class Base(DeclarativeBase):
    metadata = metadata
