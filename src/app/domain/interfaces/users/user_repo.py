from abc import ABC, abstractmethod

from app.domain.entities.user.entity import User


class UserRepo(ABC):
    @abstractmethod
    def register(self, user: User) -> User:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def logout(self) -> None:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def update_user(self, email: str, code: int) -> None:
        pass
