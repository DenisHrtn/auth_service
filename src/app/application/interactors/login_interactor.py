from app.application.use_cases.login import LoginUseCase
from app.infra.repos.users.user_repo_impl import UserRepoImpl
from app.infra.unit_of_work.async_sql import UnitOfWork


class LoginInteractor(LoginUseCase):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, email: str, password: str):
        async with self.uow as unit:
            user_repo = UserRepoImpl(unit._session)

            login_user = await user_repo.login(email, password)

            return login_user
