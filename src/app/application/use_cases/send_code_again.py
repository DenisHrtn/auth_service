from abc import ABC, abstractmethod


class SendCodeAgainUseCase(ABC):
    """
    Use case для повторной отправки кода
    """

    @abstractmethod
    def send_code_again(self, email: str) -> None:  # TODO: передавать DTO-класс
        pass
