from app.application.use_cases.logout.logout import LogoutUseCase
from app.domain.interfaces.auth.auth_interface import IAuthInterface


class LogoutInteractor(LogoutUseCase):
    def __init__(self, auth_service: IAuthInterface):
        self.auth_service = auth_service

    async def logout(self, token: str):
        self.auth_service.deactivate_token(token)

        return "Successfully logged out"
