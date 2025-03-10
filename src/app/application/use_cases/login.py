from abc import ABC, abstractmethod


class LoginUseCase(ABC):
    @abstractmethod
    def execute(self, email: str, password: str):  # TODO: передавать DTO-класс
        pass
