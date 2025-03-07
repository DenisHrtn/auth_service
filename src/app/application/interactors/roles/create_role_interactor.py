from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.roles.create_role import CreateRoleUseCase
from app.domain.entities.role.dto import RoleCreatedDTO, RoleDTO
from app.infra.repos.roles.role_repo_impl import RoleRepoImpl

from .exceptions import RoleAlreadyExists, UserAlreadyHasRole


class CreateRoleInteractor(CreateRoleUseCase):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, dto: RoleCreatedDTO) -> RoleDTO:
        async with self.uow(auto_commit=True) as unit:
            role_repo = RoleRepoImpl(unit.session)

            existing_role = await role_repo.get_by_name(dto.role_name)

            if existing_role is None:
                raise RoleAlreadyExists("Роль уже существуте!")

            user_has_role = await role_repo.check_user_role(dto.user_id)

            if user_has_role:
                raise UserAlreadyHasRole("Пользователь уже имеет роль!")

            new_role = await role_repo.create(dto)

            return new_role
