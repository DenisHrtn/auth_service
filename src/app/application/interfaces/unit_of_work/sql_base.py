from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    """
    Интерфейс класса для Uow
    """

    def __call__(self, auto_commit: bool, *args, **kwargs):
        self._auto_commit = auto_commit

        return self

    async def __aenter__(self):
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, *args, **kwargs
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            if self._auto_commit:
                await self.commit()

        await self.close()

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
