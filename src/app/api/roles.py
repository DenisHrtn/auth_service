from fastapi import APIRouter, Depends, Request

from app.application.interactors.roles.create_role_interactor import (
    CreateRoleInteractor,
)
from app.containers import container
from app.domain.entities.role.dto import RoleCreatedDTO
from app.infra.utils.auth_required import auth_required

router = APIRouter(tags=["roles"])


@router.post("/create-role")
@auth_required
async def create_role(
    request: Request,
    dto: RoleCreatedDTO,
    create_role_interactor: CreateRoleInteractor = Depends(
        lambda: container.create_role_interactor()
    ),
):
    new_role = await create_role_interactor.execute(dto)
    return {"message": "Role created successfully", "role": new_role}
