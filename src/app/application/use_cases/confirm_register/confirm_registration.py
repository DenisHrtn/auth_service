from abc import ABC, abstractmethod

from .dto import ConfirmRegisterDTO


class ConfirmRegistrationUseCase(ABC):
    @abstractmethod
    def confirm(self, dto: ConfirmRegisterDTO) -> None:
        pass
