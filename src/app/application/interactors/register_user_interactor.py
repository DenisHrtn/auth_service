from datetime import datetime

from app.application.interactors.exceptions import UserExistsException
from app.application.use_cases.register_user import RegisterUserUseCase
from app.domain.entities.user.entity import User
from app.infra.repos.users.user_repo_impl import UserRepoImpl
from app.infra.security.password_hasher import hash_password
from app.infra.unit_of_work.async_sql import UnitOfWork


class RegisterUserInteractor(RegisterUserUseCase):
    def __init__(self, uow: UnitOfWork):
        """
        Инжектим Unit of Work, из которого потом создаём репозиторий.
        """
        self.uow = uow

    async def execute(self, email: str, username: str, password: str) -> User:
        async with self.uow as unit:
            user_repo = UserRepoImpl(unit._session)

            existing_user = await user_repo.get_user_by_email(email)
            if existing_user is not None:
                raise UserExistsException("Пользователь с таким email уже существует")

            hashed_pass = hash_password(password)

            new_user = User.register(
                email=email, username=username, password=hashed_pass
            )

            new_user.code_created_at = datetime.utcnow()
            new_user.is_active = False
            new_user.is_admin = False

            registered_user = await user_repo.register(new_user)

            await unit.commit()

            return registered_user
