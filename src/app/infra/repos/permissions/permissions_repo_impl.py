from sqlalchemy import select

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.domain.interfaces.permissions.permissions_repo import PermissionsRepo
from app.infra.repos.sqla.models import Permission


class PermissionsRepoImpl(PermissionsRepo):
    def __init__(self, uow: IUnitOfWork):
        super().__init__(uow)

    async def get_permissions(self):
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session
            result = await session_.execute(select(Permission))

            permissions = result.scalars().all()

            return permissions

    async def update_permission(self, permission_model: Permission, **kwargs) -> str:
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session

            permissions_model = await session_.merge(permission_model)

            for key, value in kwargs.items():
                setattr(permissions_model, key, value)

            await session_.flush()
            await session_.commit()
            await session_.refresh(permissions_model)

            return "Successfully updated permission"

    async def get_permission_by_id(self, permission_id: int):
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session
            result = await session_.execute(
                select(Permission).filter(Permission.id == permission_id)
            )
            permission_model = result.scalars().first()

            if not permission_model:
                return None

            return permission_model
