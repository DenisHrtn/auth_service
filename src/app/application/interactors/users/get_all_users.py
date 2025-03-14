from typing import Optional

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.users.get_all_users import GetAllUsersUseCase
from app.domain.interfaces.users.user_repo import UserRepo


class GetAllUsersInteractor(GetAllUsersUseCase):
    def __init__(self, uow: IUnitOfWork, user_repo: UserRepo):
        self.uow = uow
        self.user_repo = user_repo

    async def get_all_users(
        self,
        offset: int,
        limit: int,
        is_admin: Optional[bool] = None,
        order_by: Optional[str] = None,
    ) -> list:
        users = await self.user_repo.get_all_user(
            offset=offset, limit=limit, is_admin=is_admin, order_by=order_by
        )

        return users
