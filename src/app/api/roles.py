from fastapi import APIRouter, Depends, Request, Response

from app.application.interactors.roles.gel_all_roles_interactor import (
    GetAllRolesInteractor,
)
from app.application.interactors.roles.update_role import UpdateRoleInteractor
from app.containers import container
from app.domain.entities.role.dto import UpdateRoleRTO
from app.infra.schemas.role_schemas import UpdateRoleSchema
from app.infra.utils.auth_required import auth_required

router = APIRouter(tags=["roles"])


@router.get("/get-all-roles")
@auth_required
async def gel_all_roles(
    request: Request,
    roles_interactor: GetAllRolesInteractor = Depends(
        lambda: container.get_all_roles_interactor()
    ),
):
    token = request.headers.get("Authorization")
    extracted_token = token.split(" ")[1]

    return await roles_interactor.get_all_roles(extracted_token)


@router.patch("/update-role")
@auth_required
async def update_role(
    request: Request,
    schema: UpdateRoleSchema,
    roles_interactor: UpdateRoleInteractor = Depends(
        lambda: container.update_role_interactor()
    ),
):
    token = request.headers.get("Authorization")
    extracted_token = token.split(" ")[1]

    update_dto = UpdateRoleRTO(schema.role_name, schema.description, schema.permissions)

    result = await roles_interactor.execute(extracted_token, update_dto)

    return Response(f"Role updated: {result}", status_code=200)
