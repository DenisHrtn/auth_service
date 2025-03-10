from app.application.interactors.send_code_again.exceptions import (
    UserAlreadyActiveException,
    UserNotFoundException,
)
from app.application.interfaces.confirm_code.confirm_code import IConfirmCode
from app.application.interfaces.email.dto import SendEMailDTO
from app.application.interfaces.email.email_service import IEmailService
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.send_code_again.dto import (
    SendCodeAgainDTO,
    SendCodeAgainOutputDTO,
)
from app.application.use_cases.send_code_again.send_code_again import (
    SendCodeAgainUseCase,
)
from app.domain.interfaces.users.user_repo import UserRepo


class SendCodeAgainInteractor(SendCodeAgainUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        email_sender: IEmailService,
        code_service: IConfirmCode,
        user_repo: UserRepo,
    ):
        self.uow = uow
        self.email_sender = email_sender
        self.code_service = code_service
        self.user_repo = user_repo

    async def send_code_again(self, dto: SendCodeAgainDTO) -> SendCodeAgainOutputDTO:
        existing_user = await self.user_repo.get_user_by_email(dto.email)

        if existing_user is None:
            raise UserNotFoundException("Пользователь с таким email не найден")

        if existing_user.is_active:
            raise UserAlreadyActiveException("Пользователь уже активный!")

        code = self.code_service.confirm_code()

        email_dto = SendEMailDTO(
            dto.email,
            body=(
                f"Здравствуйте!\n\n"
                f"Повторный код для подтверждения!.\n\n"
                f"Ваш уникальный код подтверждения: **{code}**\n\n"
                f"С уважением,\nКоманда проекта"
            ),
            code=code,
        )

        await self.email_sender.send_email(email_dto)

        output_dto = SendCodeAgainOutputDTO(email_dto.to_address, code)

        await self.user_repo.send_code_again(output_dto)

        return output_dto
