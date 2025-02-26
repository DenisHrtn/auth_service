from app.application.interactors.exceptions import (
    InvalidCodeException,
    UserExistsException,
)
from app.application.use_cases.confirm_registration import ConfirmRegistration
from app.infra.repos.users.user_repo_impl import UserRepoImpl
from app.infra.unit_of_work.async_sql import UnitOfWork


class ConfirmRegistrationInteractor(ConfirmRegistration):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def confirm(self, email: str, code: int) -> str:
        async with self.uow as unit:
            user_repo = UserRepoImpl(unit._session)

            existing_user = await user_repo.get_user_by_email(email)

            if not existing_user:
                raise UserExistsException("Пользователь с таким email не существует")

            if existing_user.code != code:
                raise InvalidCodeException("Неверный код подтверждения")

            await user_repo.update_user(user_model=existing_user, is_active=True)

            return "Successfully!"
