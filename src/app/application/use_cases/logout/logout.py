from abc import ABC, abstractmethod


class LogoutUseCase(ABC):
    @abstractmethod
    def logout(self, token: str):
        pass
