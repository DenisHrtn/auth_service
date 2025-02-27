from abc import ABC, abstractmethod


class ConfirmRegistrationUseCase(ABC):
    @abstractmethod
    def confirm(self, email: str, code: int) -> None:
        pass
