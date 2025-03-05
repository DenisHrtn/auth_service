from abc import ABC, abstractmethod

from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.send_code_again.dto import SendCodeAgainOutputDTO
from app.domain.entities.user.dto import UserDTO
from app.domain.entities.user.entity import User


class UserRepo(ABC):
    @abstractmethod
    def register(self, dto: RegisterUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> dict:
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

    @abstractmethod
    def send_code_again(self, dto: SendCodeAgainOutputDTO) -> str:
        pass
