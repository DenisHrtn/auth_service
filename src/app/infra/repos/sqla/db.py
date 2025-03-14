from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import DBConfig


class Database:
    def __init__(self, config: DBConfig) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=f"postgresql+asyncpg://{config.postgres_user}:"
            f"{config.postgres_password}"
            f"@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
