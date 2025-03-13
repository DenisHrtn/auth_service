from abc import ABC, abstractmethod

from .dto import ChangePasswordDto


class ChangePasswordUseCase(ABC):
    @abstractmethod
    def execute(self, dto: ChangePasswordDto):
        pass
