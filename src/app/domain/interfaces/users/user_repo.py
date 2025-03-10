from abc import ABC, abstractmethod

from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.send_code_again.dto import SendCodeAgainOutputDTO
from app.domain.entities.user.dto import UserDTO
from app.domain.entities.user.entity import User


class UserRepo(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def register(self, dto: RegisterUserDTO) -> UserDTO:
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> dict:
        pass

    @abstractmethod
    async def logout(self) -> None:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def update_user(self, email: str, code: int) -> None:
        pass

    @abstractmethod
    async def send_code_again(self, dto: SendCodeAgainOutputDTO) -> str:
        pass
