from app.application.interactors.exceptions import UserExistsException
from app.application.interfaces.email.dto import SendEMailDTO
from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.register.register_user import RegisterUserUseCase
from app.domain.entities.user.dto import UserDTO
from app.infra.repos.users.user_repo_impl import UserRepoImpl
from app.infra.services.celery_email_sender import CeleryEmailSender
from app.infra.services.password_hasher import PasswordHasher
from app.infra.unit_of_work.async_sql import UnitOfWork


class RegisterUserInteractor(RegisterUserUseCase):
    def __init__(self, uow: UnitOfWork, email_sender: CeleryEmailSender):
        """
        Инжектим Unit of Work, из которого потом создаём репозиторий.
        """
        self.uow = uow
        self.email_sender = email_sender
        self.password_hasher = PasswordHasher()

    async def execute(self, dto: RegisterUserDTO) -> UserDTO:
        async with self.uow(auto_commit=True) as unit:
            user_repo = UserRepoImpl(unit._session)

            existing_user = await user_repo.get_user_by_email(dto.email)
            if existing_user is not None:
                raise UserExistsException("Пользователь с таким email уже существует")

            hashed_pass = self.password_hasher.hash_password(dto.password)

            new_user = RegisterUserDTO(
                email=dto.email, username=dto.username, password=hashed_pass
            )

            registered_user = await user_repo.register(new_user)

            email_dto = SendEMailDTO(
                to_address=registered_user.email, code=registered_user.code
            )
            await self.email_sender.send_email(email_dto)

            return registered_user
