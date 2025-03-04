from app.application.interfaces.email.dto import SendEMailDTO
from app.application.interfaces.email.email_service import IEmailService
from app.infra.celery.tasks import send_confirm_code_to_email


class CeleryEmailSender(IEmailService):
    async def send_email(self, dto: SendEMailDTO):
        send_confirm_code_to_email.delay(dto.to_address, dto.code)
