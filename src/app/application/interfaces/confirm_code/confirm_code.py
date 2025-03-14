from abc import ABC, abstractmethod


class IConfirmCode(ABC):
    @abstractmethod
    def confirm_code(self) -> int:
        pass
