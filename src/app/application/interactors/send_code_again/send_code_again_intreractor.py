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
from app.infra.repos.users.user_repo_impl import UserRepoImpl


class SendCodeAgainInteractor(SendCodeAgainUseCase):
    def __init__(
        self, uow: IUnitOfWork, email_sender: IEmailService, code_service: IConfirmCode
    ):
        self.uow = uow
        self.email_sender = email_sender
        self.code_service = code_service

    async def send_code_again(self, dto: SendCodeAgainDTO) -> SendCodeAgainOutputDTO:
        async with self.uow(auto_commit=True) as unit:
            user_repo = UserRepoImpl(unit.session)

            existing_user = await user_repo.get_user_by_email(dto.email)

            if existing_user is None:
                raise UserNotFoundException("Пользователь с таким email не найден")

            if existing_user.is_active:
                raise UserAlreadyActiveException("Пользователь уже активный!")

            code = self.code_service.confirm_code()

            email_dto = SendEMailDTO(dto.email, code)

            await self.email_sender.send_email(email_dto)

            output_dto = SendCodeAgainOutputDTO(email_dto.to_address, code)

            return output_dto
