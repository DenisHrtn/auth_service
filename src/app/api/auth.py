from fastapi import APIRouter, Depends, HTTPException

from app.application.interactors.confirm_register.confirm_register_interactor import (
    ConfirmRegistrationInteractor,
)
from app.application.interactors.login_interactor import LoginInteractor
from app.application.interactors.register.register_user_interactor import (
    RegisterUserInteractor,
)
from app.application.interactors.send_code_again.send_code_again_intreractor import (
    SendCodeAgainInteractor,
)
from app.application.use_cases.confirm_register.dto import ConfirmRegisterDTO
from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.send_code_again.dto import SendCodeAgainDTO
from app.containers import container
from app.infra.schemas.auth_schemas import (
    ConfirmRegistrationRequestSchema,
    LoginRequestSchema,
    RegisterRequestSchema,
    SendCodeAgainRequestSchema,
)
from app.infra.security.get_current_user import get_current_user

router = APIRouter(tags=["auth"])


@router.post("/register")
async def register_user(
    schema: RegisterRequestSchema,
    register_user_interactor: RegisterUserInteractor = Depends(
        lambda: container.register_user_interactor()
    ),
):
    dto = RegisterUserDTO(
        email=schema.email, username=schema.username, password=schema.password
    )
    new_user = await register_user_interactor.execute(dto)
    return {"message": "User registered successfully", "user_id": new_user.id}


@router.patch("/confirm-registration")
async def confirm_registration(
    request: ConfirmRegistrationRequestSchema,
    confirm_registration_interactor: ConfirmRegistrationInteractor = Depends(
        lambda: container.confirm_registration_interactor()
    ),
):
    confirm_dto = ConfirmRegisterDTO(email=request.email, code=request.code)

    updated_user = await confirm_registration_interactor.confirm(confirm_dto)
    return {"message": f"User confirmed successfully, email: {updated_user}"}


@router.patch("/send-code-again")
async def send_code_again(
    request: SendCodeAgainRequestSchema,
    send_code_again_interactor: SendCodeAgainInteractor = Depends(
        lambda: container.send_code_again_interactor()
    ),
):
    try:
        dto = SendCodeAgainDTO(request.email)

        new_updated_user = await send_code_again_interactor.send_code_again(dto)
        return {"message": f"User sent code again, email: {new_updated_user}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    request: LoginRequestSchema,
    login_interactor: LoginInteractor = Depends(lambda: container.login_interactor()),
):
    try:
        result = await login_interactor.execute(
            email=request.username, password=request.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/protected-route")
async def protected_route(user_id: str = Depends(get_current_user)):
    return {"message": "You are authenticated!", "user_id": user_id}
