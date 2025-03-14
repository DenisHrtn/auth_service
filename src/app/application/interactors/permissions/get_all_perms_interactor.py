from app.application.interfaces.decode_token.decode_tokens import IDecodeJWTToken
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.permissions.get_all_permissions import (
    GetAllPermissionsUseCase,
)
from app.domain.interfaces.permissions.permissions_repo import PermissionsRepo


class GetAllPermissionsInteractor(GetAllPermissionsUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        decode_service: IDecodeJWTToken,
        permissions_repo: PermissionsRepo,
    ):
        self.uow = uow
        self.decode_service = decode_service
        self.permissions_repo = permissions_repo

    async def get_all_permissions(self, token: str):
        is_admin = await self.decode_service.check_is_admin(token)

        if is_admin == "admin":
            permissions = await self.permissions_repo.get_permissions()

            return permissions

        return "You don't have permission to perform this action"
