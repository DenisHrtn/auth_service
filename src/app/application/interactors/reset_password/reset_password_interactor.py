from app.application.interfaces.confirm_code.confirm_code import IConfirmCode
from app.application.interfaces.email.dto import SendEMailDTO
from app.application.interfaces.email.email_service import IEmailService
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.reset_password.reset_password import ResetPasswordUseCase
from app.domain.interfaces.users.user_repo import UserRepo

from .exceptions import UserNotActive


class ResetPasswordInteractor(ResetPasswordUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        user_repo: UserRepo,
        email_sender: IEmailService,
        code_service: IConfirmCode,
    ):
        self.uow = uow
        self.user_repo = user_repo
        self.email_sender = email_sender
        self.code_service = code_service

    async def reset_password(self, email: str):
        existing_user = await self.user_repo.get_user_by_email(email)

        if not existing_user.is_active:
            raise UserNotActive("User is not active")

        code = self.code_service.confirm_code()

        email_dto = SendEMailDTO(
            email,
            body=(
                f"Здравствуйте, {email}\n\n"
                f"Код подтверждения для смены пароля: {code}"
            ),
            code=code,
        )

        await self.email_sender.send_email(email_dto)

        await self.user_repo.update_user(existing_user, code=code)

        return "Successfully reset password"
