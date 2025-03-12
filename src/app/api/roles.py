from fastapi import APIRouter, Depends, Request

from app.application.interactors.roles.gel_all_roles_interactor import (
    GetAllRolesInteractor,
)
from app.containers import container
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

    if not token or not token.startswith("Bearer "):
        return {"detail": "Missing or invalid token"}

    extracted_token = token.split(" ")[1]

    return await roles_interactor.get_all_roles(extracted_token)
