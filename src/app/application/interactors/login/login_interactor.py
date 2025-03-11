from app.application.interfaces.login.dto import AuthTokenDTO, VerifyPasswordDTO
from app.application.interfaces.login.login_interface import ILoginInterface
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.login import LoginUseCase
from app.domain.interfaces.auth.auth_interface import IAuthInterface
from app.domain.interfaces.users.user_repo import UserRepo


class LoginInteractor(LoginUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        user_repo: UserRepo,
        jwt_auth_service: IAuthInterface,
        login_inter: ILoginInterface,
    ):
        self.uow = uow
        self.user_repo = user_repo
        self.jwt_auth_service = jwt_auth_service
        self.login_inter = login_inter

    async def execute(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_user_by_email(email)

        verify_pass_dto = VerifyPasswordDTO(password, user.hashed_password)

        if not await self.login_inter.verify_password(verify_pass_dto):
            raise ValueError("Пароли не совпадают")

        login_user = await self.user_repo.login(email, password)

        auth_token_dto = AuthTokenDTO(user.id, user.email, login_user)

        access_token = await self.login_inter.create_access_token(auth_token_dto)
        refresh_token = await self.login_inter.create_refresh_token(auth_token_dto)

        await self.jwt_auth_service.put_token_in_redis(access_token)

        return {"access_token": access_token, "refresh_token": refresh_token}
