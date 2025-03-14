from abc import ABC, abstractmethod

from app.application.interfaces.email.dto import SendEMailDTO


class IEmailService(ABC):
    @abstractmethod
    async def send_email(self, dto: SendEMailDTO):
        pass
