from abc import ABC, abstractmethod

from src.app.domain.users.entities import User


class IUsersRepo(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass
