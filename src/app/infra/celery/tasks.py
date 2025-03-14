import logging

from app.infra.services.email_service import send_email_via_ses
from app.infra.services.exceptions import SendMessageError

from .celery_app import app

logger = logging.getLogger(__name__)


@app.task
def send_confirm_code_to_email(to_address: str, body: str, code: int) -> None:
    """
    Таска для отправки кода подтверждения на почту при регистрации
    """

    try:
        send_email_via_ses(
            to_address=to_address, body=body, subject=f"fКод подтверждения: {code}"
        )

        logger.info(f"Письмо с приглашением успешно отправлено на {to_address}")
    except SendMessageError as exc:
        raise SendMessageError(str(exc)) from exc
