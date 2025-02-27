from app.application.interactors.exceptions import (
    UserAlreadyActiveException,
    UserNotFoundException,
)
from app.application.use_cases.send_code_again import SendCodeAgainUseCase
from app.infra.repos.users.user_repo_impl import UserRepoImpl
from app.infra.unit_of_work.async_sql import UnitOfWork


class SendCodeAgainInteractor(SendCodeAgainUseCase):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def send_code_again(self, email: str) -> str:
        async with self.uow as unit:
            user_repo = UserRepoImpl(unit._session)

            existing_user = await user_repo.get_user_by_email(email)

            if existing_user is None:
                raise UserNotFoundException("Пользователь с таким email не найден")

            if existing_user.is_active:
                raise UserAlreadyActiveException("Пользователь уже активный!")

            await user_repo.send_code_again(email=email)

            return "Successfully!"
