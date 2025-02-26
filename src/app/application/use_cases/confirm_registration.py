from abc import ABC, abstractmethod


class ConfirmRegistration(ABC):
    @abstractmethod
    def confirm(self, email: str, code: int) -> None:
        pass
