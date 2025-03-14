from abc import ABC, abstractmethod


class ResetPasswordUseCase(ABC):
    @abstractmethod
    async def reset_password(self, email: str) -> str:
        pass
