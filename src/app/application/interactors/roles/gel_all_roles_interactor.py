from app.application.interfaces.decode_token.decode_tokens import IDecodeJWTToken
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.roles.get_all_roles import GetAllRolesUseCase
from app.domain.interfaces.roles.role_repo import RoleRepo


class GetAllRolesInteractor(GetAllRolesUseCase):
    def __init__(
        self, uow: IUnitOfWork, decode_service: IDecodeJWTToken, role_repo: RoleRepo
    ):
        self.uow = uow
        self.decode_service = decode_service
        self.role_repo = role_repo

    async def get_all_roles(self, token: str):
        is_admin = await self.decode_service.check_is_admin(token)

        if is_admin == "admin":
            roles = await self.role_repo.get_all_roles()

            return roles

        return "Unauthorized"
