import logging

from app.infra.services.email_service import send_email_via_ses
from app.infra.services.exceptions import SendMessageError

from .celery_app import app

logger = logging.getLogger(__name__)


@app.task
def send_confirm_code_to_email(to_address: str, code: int) -> None:
    """
    Таска для отправки кода подтверждения на почту при регистрации
    """

    try:
        body = (
            f"Здравствуйте!\n\n"
            f"Вы успешно прошли регистрацию!.\n\n"
            f"Ваш уникальный код подтверждения: **{code}**\n\n"
            f"С уважением,\nКоманда проекта"
        )

        send_email_via_ses(
            to_address=to_address, body=body, subject="Код подтверждения"
        )

        logger.info(f"Письмо с приглашением успешно отправлено на {to_address}")
    except SendMessageError as exc:
        raise SendMessageError(str(exc)) from exc
