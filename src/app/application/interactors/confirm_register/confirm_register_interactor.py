from app.application.interactors.confirm_register.exceptions import (
    InvalidCodeException,
    UserAlreadyActiveException,
    UserExistsException,
)
from app.application.interfaces.confirm_code.confirm_code import IConfirmCode
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.confirm_register.confirm_registration import (
    ConfirmRegistrationUseCase,
)
from app.application.use_cases.confirm_register.dto import ConfirmRegisterDTO
from app.domain.interfaces.users.user_repo import UserRepo


class ConfirmRegistrationInteractor(ConfirmRegistrationUseCase):
    def __init__(
        self, uow: IUnitOfWork, code_service: IConfirmCode, user_repo: UserRepo
    ):
        self.uow = uow
        self.code_service = code_service
        self.user_repo = user_repo

    async def confirm(self, dto: ConfirmRegisterDTO) -> str:
        existing_user = await self.user_repo.get_user_by_email(dto.email)

        if not existing_user:
            raise UserExistsException("Пользователь с таким email не существует")

        if existing_user.is_active:
            raise UserAlreadyActiveException("Пользователь уже зарегистрирован!")

        if existing_user.code != dto.code:
            raise InvalidCodeException("Неверный код подтверждения")

        await self.user_repo.update_user(user_model=existing_user, is_active=True)

        return "Successfully!"
