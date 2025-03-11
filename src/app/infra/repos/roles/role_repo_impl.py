from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.role.dto import RoleDTO
from app.domain.interfaces.roles.role_repo import RoleRepo
from app.infra.repos.sqla.models import Role


class RoleRepoImpl(RoleRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, role_name: str) -> Optional[Role]:
        result = await self.session.execute(
            select(Role).filter(Role.role_name == role_name)
        )
        role_model = result.scalars().first()

        if not role_model:
            return None

        return role_model

    async def check_user_role(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(exists().where(Role.user_id == user_id))
        )
        exists_ = result.scalar()

        if not exists_:
            return False

        return True

    async def update_role(self, role_id: int, role: RoleDTO) -> RoleDTO:
        return "Not Implemented"
