from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.orm import joinedload

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.domain.entities.role.dto import map_role_to_dto
from app.domain.interfaces.roles.role_repo import RoleRepo
from app.infra.repos.sqla.models import Role


class RoleRepoImpl(RoleRepo):
    def __init__(self, uow: IUnitOfWork):
        super().__init__(uow)

    async def get_by_name(self, role_name: str) -> Optional[Role]:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session
            result = await session_.execute(
                select(Role).filter(Role.role_name == role_name)
            )
            role_model = result.scalars().first()

            if not role_model:
                return None

            return role_model

    async def check_user_role(self, user_id: int) -> bool:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session
            result = await session_.execute(
                select(exists().where(Role.user_id == user_id))
            )
            exists_ = result.scalar()

            if not exists_:
                return False

            return True

    async def update_role(self, role_model: Role, **kwargs) -> str:
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session

            role_model = await session_.merge(role_model)

            for key, value in kwargs.items():
                setattr(role_model, key, value)

            await session_.flush()
            await session_.commit()
            await session_.refresh(role_model)

            return "Success"

    async def get_all_roles(self):
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session
            result = await session_.execute(select(Role).options(joinedload(Role.user)))

            roles = result.scalars().all()

            return [map_role_to_dto(role) for role in roles]
