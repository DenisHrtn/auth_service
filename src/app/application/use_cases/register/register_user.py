from abc import ABC, abstractmethod

from app.application.use_cases.register.dto import RegisterUserDTO
from app.domain.entities.user.dto import UserDTO


class RegisterUserUseCase(ABC):
    @abstractmethod
    def execute(self, register_dto: RegisterUserDTO) -> UserDTO:
        pass
