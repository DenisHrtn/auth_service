from app.application.use_cases.login import LoginUseCase
from app.domain.interfaces.users.user_repo import UserRepo
from app.infra.unit_of_work.async_sql import UnitOfWork


class LoginInteractor(LoginUseCase):
    def __init__(self, uow: UnitOfWork, user_repo: UserRepo):
        self.uow = uow
        self.user_repo = user_repo

    async def execute(self, email: str, password: str):
        login_user = await self.user_repo.login(email, password)

        return login_user
