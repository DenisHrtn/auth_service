from abc import ABC, abstractmethod

from .dto import SendCodeAgainDTO, SendCodeAgainOutputDTO


class SendCodeAgainUseCase(ABC):
    """
    Use case для повторной отправки кода
    """

    @abstractmethod
    def send_code_again(self, dto: SendCodeAgainDTO) -> SendCodeAgainOutputDTO:
        pass
