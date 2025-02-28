from abc import ABC, abstractmethod


class SendCodeAgainUseCase(ABC):
    @abstractmethod
    def send_code_again(self, email: str) -> None:
        pass
