from fastapi import APIRouter, Depends, Request

from app.application.interactors.permissions.get_all_perms_interactor import (
    GetAllPermissionsInteractor,
)
from app.application.interactors.permissions.update_permission_interactor import (
    UpdatePermissionInteractor,
)
from app.containers import container
from app.domain.entities.permission.dto import UpdatePermissionDto
from app.infra.schemas.permission_schemas import UpdatePermissionsRequest
from app.infra.utils.auth_required import auth_required

router = APIRouter(tags=["permissions"])


@router.get("/get-permissions")
@auth_required
async def get_all_permissions(
    request: Request,
    permissions_interactor: GetAllPermissionsInteractor = Depends(
        lambda: container.get_all_permissions_interactor()
    ),
):
    token = request.headers.get("Authorization")
    extracted_token = token.split(" ")[1]

    return await permissions_interactor.get_all_permissions(extracted_token)


@router.patch("/update-permissions/{permission_id}")
@auth_required
async def update_permissions(
    permission_id: int,
    request: Request,
    schema: UpdatePermissionsRequest,
    permissions_interactor: UpdatePermissionInteractor = Depends(
        lambda: container.update_permissions_interactor()
    ),
):
    token = request.headers.get("Authorization")
    extracted_token = token.split(" ")[1]

    dto = UpdatePermissionDto(schema.description)

    return await permissions_interactor.execute(permission_id, extracted_token, dto)
