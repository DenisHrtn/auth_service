from typing import Optional

from fastapi import APIRouter, Depends, Query, Request

from app.application.interactors.users.get_all_users import GetAllUsersInteractor
from app.containers import container
from app.infra.utils.auth_required import auth_required

router = APIRouter(tags=["users"])


@router.get("/users")
@auth_required
async def get_all_users(
    request: Request,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    is_admin: Optional[bool] = Query(None),
    order_by: Optional[str] = Query(None, regex="^(date|name|role)$"),
    get_all_users_interactor: GetAllUsersInteractor = Depends(
        lambda: container.get_all_users_interactor()
    ),
):
    result = await get_all_users_interactor.get_all_users(
        offset=offset,
        limit=limit,
        is_admin=is_admin,
        order_by=order_by,
    )

    return result
