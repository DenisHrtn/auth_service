from dataclasses import asdict

from app.application.interfaces.decode_token.decode_tokens import IDecodeJWTToken
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.permissions.update_permission import (
    UpdatePermissionUseCase,
)
from app.domain.entities.permission.dto import UpdatePermissionDto
from app.domain.interfaces.permissions.permissions_repo import PermissionsRepo

from .exceptions import PermissionNotFound


class UpdatePermissionInteractor(UpdatePermissionUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        permission_repo: PermissionsRepo,
        decode_service: IDecodeJWTToken,
    ):
        self.uow = uow
        self.permission_repo = permission_repo
        self.decode_service = decode_service

    async def execute(
        self, permission_id: int, token: str, dto: UpdatePermissionDto
    ) -> str:
        is_admin = await self.decode_service.check_is_admin(token)

        if is_admin == "admin":
            existing_permission = await self.permission_repo.get_permission_by_id(
                permission_id
            )

            if not existing_permission:
                raise PermissionNotFound("Permission not found")

            await self.permission_repo.update_permission(
                permission_model=existing_permission, **asdict(dto)
            )

            return "Successfully updated permission"

        return "You don't have permission to perform this action"
