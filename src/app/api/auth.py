from fastapi import APIRouter, Depends, HTTPException

from app.application.interactors.register_user_interactor import RegisterUserInteractor
from app.containers import container
from app.infra.schemas.auth_schemas import RegisterRequest

router = APIRouter()


@router.post("/register")
async def register_user(
    request: RegisterRequest,
    register_user_interactor: RegisterUserInteractor = Depends(
        lambda: container.register_user_interactor()
    ),
):
    try:
        new_user = await register_user_interactor.execute(
            request.email, request.username, request.password
        )
        return {"message": "User registered successfully", "user_id": new_user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
