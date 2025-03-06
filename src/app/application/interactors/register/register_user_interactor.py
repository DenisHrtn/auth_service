from app.application.interactors.register.exceptions import UserExistsException
from app.application.interfaces.email.dto import SendEMailDTO
from app.application.interfaces.email.email_service import IEmailService
from app.application.interfaces.password_hash.dto import PasswordHashDTO
from app.application.interfaces.password_hash.password_hasher import IPasswordHasher
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.register.register_user import RegisterUserUseCase
from app.domain.entities.user.dto import UserDTO
from app.infra.repos.users.user_repo_impl import UserRepoImpl


class RegisterUserInteractor(RegisterUserUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        email_sender: IEmailService,
        password_hasher: IPasswordHasher,
    ):
        """
        Инжектим Unit of Work, из которого потом создаём репозиторий.
        """
        self.uow = uow
        self.email_sender = email_sender
        self.password_hasher = password_hasher

    async def execute(self, register_dto: RegisterUserDTO) -> UserDTO:
        async with self.uow(auto_commit=True) as unit:
            user_repo = UserRepoImpl(unit.session)

            existing_user = await user_repo.get_user_by_email(register_dto.email)
            if existing_user is not None:
                raise UserExistsException("Пользователь с таким email уже существует")

            pass_dto = PasswordHashDTO(register_dto.password)

            hashed_pass = self.password_hasher.hash_password(pass_dto)

            new_user = RegisterUserDTO(
                email=register_dto.email,
                username=register_dto.username,
                password=hashed_pass,
            )

            registered_user = await user_repo.register(new_user)

            email_dto = SendEMailDTO(
                to_address=registered_user.email, code=registered_user.code
            )
            await self.email_sender.send_email(email_dto)

            return registered_user
