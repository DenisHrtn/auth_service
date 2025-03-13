from app.application.interfaces.password_hash.dto import PasswordHashDTO
from app.application.interfaces.password_hash.password_hasher import IPasswordHasher
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.change_password.change_password import (
    ChangePasswordUseCase,
)
from app.application.use_cases.change_password.dto import ChangePasswordDto
from app.domain.interfaces.users.user_repo import UserRepo


class ChangePasswordInteractor(ChangePasswordUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        user_repo: UserRepo,
        password_hasher: IPasswordHasher,
    ):
        self.uow = uow
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def execute(self, dto: ChangePasswordDto):
        existing_user = await self.user_repo.get_user_by_code(code=dto.code)

        new_password = dto.password

        pass_dto = PasswordHashDTO(new_password)

        hashed_pass = self.password_hasher.hash_password(pass_dto)

        await self.user_repo.update_user(existing_user, hashed_password=hashed_pass)

        return "Successfully updated password"
