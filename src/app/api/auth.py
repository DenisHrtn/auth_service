from fastapi import APIRouter, Depends, HTTPException

from app.application.interactors.change_password.change_password_interactor import (
    ChangePasswordInteractor,
)
from app.application.interactors.confirm_register.confirm_register_interactor import (
    ConfirmRegistrationInteractor,
)
from app.application.interactors.login.login_interactor import LoginInteractor
from app.application.interactors.register.register_user_interactor import (
    RegisterUserInteractor,
)
from app.application.interactors.reset_password.reset_password_interactor import (
    ResetPasswordInteractor,
)
from app.application.interactors.send_code_again.send_code_again_intreractor import (
    SendCodeAgainInteractor,
)
from app.application.use_cases.change_password.dto import ChangePasswordDto
from app.application.use_cases.confirm_register.dto import ConfirmRegisterDTO
from app.application.use_cases.register.dto import RegisterUserDTO
from app.application.use_cases.send_code_again.dto import SendCodeAgainDTO
from app.containers import container
from app.infra.schemas.auth_schemas import (
    ChangePasswordSchema,
    ConfirmRegistrationRequestSchema,
    LoginRequestSchema,
    RegisterRequestSchema,
    ResetPasswordSchema,
    SendCodeAgainRequestSchema,
)

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
    schema: ConfirmRegistrationRequestSchema,
    confirm_registration_interactor: ConfirmRegistrationInteractor = Depends(
        lambda: container.confirm_registration_interactor()
    ),
):
    confirm_dto = ConfirmRegisterDTO(email=schema.email, code=schema.code)

    updated_user = await confirm_registration_interactor.confirm(confirm_dto)
    return {"message": f"User confirmed successfully, email: {updated_user}"}


@router.patch("/send-code-again")
async def send_code_again(
    schema: SendCodeAgainRequestSchema,
    send_code_again_interactor: SendCodeAgainInteractor = Depends(
        lambda: container.send_code_again_interactor()
    ),
):
    try:
        dto = SendCodeAgainDTO(schema.email)

        new_updated_user = await send_code_again_interactor.send_code_again(dto)
        return {"message": f"User sent code again, email: {new_updated_user}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    schema: LoginRequestSchema,
    login_interactor: LoginInteractor = Depends(lambda: container.login_interactor()),
):
    try:
        result = await login_interactor.execute(
            email=schema.email, password=schema.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset-password")
async def reset_password(
    schema: ResetPasswordSchema,
    reset_password_interactor: ResetPasswordInteractor = Depends(
        lambda: container.reset_password_interactor()
    ),
):
    result = await reset_password_interactor.reset_password(schema.email)

    return result


@router.patch("/change-password")
async def change_password(
    schema: ChangePasswordSchema,
    change_password_interactor: ChangePasswordInteractor = Depends(
        lambda: container.change_password_interactor()
    ),
):
    change_pass_dto = ChangePasswordDto(
        schema.code, schema.password, schema.password_again
    )

    result = await change_password_interactor.execute(change_pass_dto)

    return result
