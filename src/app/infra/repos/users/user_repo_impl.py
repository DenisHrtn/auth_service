from typing import Optional

from sqlalchemy import select

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.send_code_again.dto import SendCodeAgainOutputDTO
from app.domain.entities.user.dto import UserDTO
from app.domain.interfaces.users.user_repo import UserRepo
from app.infra.repos.sqla.models import Role, UserModel
from app.infra.repos.users.exceptions import InvalidPassword
from app.infra.security.hash_password import verify_password
from app.infra.utils.generate_confirm_code import gen_code
from app.infra.utils.generate_tokens import create_access_token, create_refresh_token


class UserRepoImpl(UserRepo):
    def __init__(self, uow: IUnitOfWork):
        super().__init__(uow)

    async def register(self, dto: RegisterUserDTO) -> UserDTO:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session
            user_model = UserModel(
                email=dto.email,
                username=dto.username,
                hashed_password=dto.password,
                code=gen_code(),
                is_active=False,
            )

            session_.add(user_model)
            await session_.flush()

            role_model = Role(
                role_name=user_model.username,
                description="",
                permissions=[1],
                user_id=user_model.id,
            )

            session_.add(role_model)
            await session_.flush()

            user_dto = UserDTO(
                id=user_model.id,
                email=user_model.email,
                username=user_model.username,
                hashed_password=user_model.hashed_password,
                code=user_model.code,
                code_created_at=user_model.code_created_at,
                is_admin=user_model.is_admin,
                is_active=user_model.is_active,
                is_blocked=user_model.is_blocked,
                date_joined=user_model.date_joined,
            )

            return user_dto

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session
            result = await session_.execute(
                select(UserModel).filter((UserModel.email) == email)
            )
            user_model = result.scalars().first()

            if not user_model:
                return None

            return user_model

    async def update_user(self, user_model: UserModel, **kwargs):
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session

            user_model = await session_.merge(user_model)

            for key, value in kwargs.items():
                setattr(user_model, key, value)

            await session_.flush()
            await session_.commit()
            await session_.refresh(user_model)

    async def send_code_again(self, dto: SendCodeAgainOutputDTO) -> str:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session
            user = await session_.execute(
                select(UserModel).filter(UserModel.email == dto.email)
            )
            user_model = user.scalars().first()

            if not user_model:
                return "None"

            await self.update_user(user_model, code=dto.code)

            return "Code has been sent"

    async def login(self, email: str, password: str) -> dict:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session
            user = await self.get_user_by_email(email)

            result = await session_.execute(
                select(Role.role_name).where(Role.user_id == user.id)
            )
            role_name = result.scalars().first()

            if not verify_password(password, user.hashed_password):
                raise InvalidPassword("Пароли не совпадают")

            access_token = create_access_token(user.id, user.email, role_name)
            refresh_token = create_refresh_token(user.id, user.email, role_name)

            return {"access_token": access_token, "refresh_token": refresh_token}

    async def logout(self) -> None:
        # заглушка
        raise NotImplementedError("Метод logout ещё не реализован")
