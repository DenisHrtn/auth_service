from abc import ABC, abstractmethod

from app.application.use_cases.register.dto import RegisterUserDTO
from app.domain.entities.user.dto import UserDTO


class RegisterUserUseCase(ABC):
    @abstractmethod
    def execute(self, dto: RegisterUserDTO) -> UserDTO:
        pass
