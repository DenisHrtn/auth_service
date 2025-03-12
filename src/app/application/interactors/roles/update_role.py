from dataclasses import asdict

from app.application.interfaces.decode_token.decode_tokens import IDecodeJWTToken
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.roles.update_role import UpdateRoleUseCase
from app.domain.entities.role.dto import UpdateRoleRTO
from app.domain.interfaces.roles.role_repo import RoleRepo

from .exceptions import RoleNotFound


class UpdateRoleInteractor(UpdateRoleUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        role_repo: RoleRepo,
        decode_service: IDecodeJWTToken,
    ):
        self.uow = uow
        self.role_repo = role_repo
        self.decode_service = decode_service

    async def execute(self, token: str, dto: UpdateRoleRTO) -> str:
        is_admin = await self.decode_service.check_is_admin(token)

        if is_admin == "admin":
            existing_role = await self.role_repo.get_by_name(dto.role_name)

            if not existing_role:
                raise RoleNotFound(f"Role '{dto.role_name}' not found")

            await self.role_repo.update_role(role_model=existing_role, **asdict(dto))

            return "Successful"

        return "You don't have permission to perform this action"
