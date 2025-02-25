from abc import ABC, abstractmethod

from app.domain.entities.user.entity import User


class RegisterUser(ABC):
    @abstractmethod
    def execute(self, email: str, username: str, password: str) -> User:
        pass
