from fastapi import APIRouter, Depends, Request

from app.application.interactors.permissions.get_all_perms_interactor import (
    GetAllPermissionsInteractor,
)
from app.containers import container
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
