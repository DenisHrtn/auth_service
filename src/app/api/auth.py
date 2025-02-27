from fastapi import APIRouter, Depends, HTTPException

from app.application.interactors.confirm_registration_interactor import (
    ConfirmRegistrationInteractor,
)
from app.application.interactors.register_user_interactor import RegisterUserInteractor
from app.application.interactors.send_code_again_intreractor import (
    SendCodeAgainInteractor,
)
from app.containers import container
from app.infra.schemas.auth_schemas import (
    ConfirmRegistrationRequest,
    RegisterRequest,
    SendCodeAgainRequest,
)

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


@router.patch("/send-code-again")
async def send_code_again(
    request: SendCodeAgainRequest,
    send_code_again_interactor: SendCodeAgainInteractor = Depends(
        lambda: container.send_code_again_interactor()
    ),
):
    try:
        new_updated_user = await send_code_again_interactor.send_code_again(
            request.email
        )
        return {"message": f"User sent code again, email: {new_updated_user}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
