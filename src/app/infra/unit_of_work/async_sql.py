from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    """
    Provides a unit of work pattern for managing transactions and repositories in
    an asynchronous SQLAlchemy session.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        auto_commit: bool = False,
    ) -> None:
        self._session_factory = session_factory
        self._auto_commit = auto_commit

    async def __aenter__(self) -> IUnitOfWork:
        self.session = self._session_factory()
        return await super().__aenter__()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
