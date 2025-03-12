from dataclasses import asdict

from infra.unit_of_work.async_sql import UnitOfWork

from app.application.use_cases.roles.update_role import UpdateRoleUseCase
from app.domain.entities.role.dto import RoleDTO, UpdateRoleRTO
from app.domain.interfaces.roles.role_repo import RoleRepo

from .exceptions import RoleNotFound


class UpdateRoleInteractor(UpdateRoleUseCase):
    def __init__(self, uow: UnitOfWork, role_repo: RoleRepo):
        self.uow = uow
        self.role_repo = role_repo

    async def execute(self, dto: UpdateRoleRTO) -> RoleDTO:
        existing_role = await self.role_repo.get_by_name(dto.role_name)

        if not existing_role:
            raise RoleNotFound(f"Role '{dto.role_name}' not found")

        await self.role_repo.update_role(role_model=existing_role, **asdict(dto))
