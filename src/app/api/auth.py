from fastapi import APIRouter, Depends, HTTPException

from app.application.interactors.confirm_registration_interactor import (
    ConfirmRegistrationInteractor,
)
from app.application.interactors.register_user_interactor import RegisterUserInteractor
from app.containers import container
from app.infra.schemas.auth_schemas import ConfirmRegistrationRequest, RegisterRequest

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


@router.patch("/confirm-registration")
async def confirm_registration(
    request: ConfirmRegistrationRequest,
    confirm_registration_interactor: ConfirmRegistrationInteractor = Depends(
        lambda: container.confirm_registration_interactor()
    ),
):
    try:
        updated_user = await confirm_registration_interactor.confirm(
            request.email, request.code
        )
        return {"message": f"User confirmed successfully, email: {updated_user}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
