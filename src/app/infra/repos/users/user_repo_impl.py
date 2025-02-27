from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user.dto import UserDTO
from app.domain.entities.user.entity import User
from app.domain.interfaces.users.user_repo import UserRepo
from app.infra.celery.tasks import send_confirm_code_to_email
from app.infra.repos.sqla.models import UserModel
from app.infra.utils.generate_confirm_code import gen_code


class UserRepoImpl(UserRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, user: User) -> User:
        user_model = UserModel(
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_admin=user.is_admin,
            code_created_at=user.code_created_at,
            code=gen_code(),
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)

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

        send_confirm_code_to_email(to_address=user.email, code=user.code)

        return User(user_dto)

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).filter((UserModel.email) == email)
        )
        user_model = result.scalars().first()

        if not user_model:
            return None

        return user_model

    async def update_user(self, user_model: UserModel, **kwargs):
        for key, value in kwargs.items():
            setattr(user_model, key, value)

        await self.session.commit()
        await self.session.refresh(user_model)

    async def send_code_again(self, email: str) -> str:
        user = await self.session.execute(
            select(UserModel).filter(UserModel.email == email)
        )
        user_model = user.scalars().first()

        if not user_model:
            return "None"

        user_model.code = gen_code()

        await self.update_user(user_model, code=user_model.code)

        send_confirm_code_to_email(to_address=user_model.email, code=user_model.code)

        return "Code has been sent"

    async def login(self, username: str, password: str) -> User:
        # заглушка
        raise NotImplementedError("Метод login ещё не реализован")

    async def logout(self) -> None:
        # заглушка
        raise NotImplementedError("Метод logout ещё не реализован")
