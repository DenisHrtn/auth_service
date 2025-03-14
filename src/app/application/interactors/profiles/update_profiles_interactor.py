from dataclasses import asdict

from app.application.interfaces.decode_token.decode_tokens import IDecodeJWTToken
from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.profiles.dto import UpdateProfileDTO
from app.application.use_cases.profiles.update_profile import UpdateProfileUseCase
from app.domain.interfaces.profiles.profiles_repo import ProfilesRepo


class UpdateProfilesInteractor(UpdateProfileUseCase):
    def __init__(
        self,
        uow: IUnitOfWork,
        profile_repo: ProfilesRepo,
        decode_service: IDecodeJWTToken,
    ):
        self.uow = uow
        self.profile_repo = profile_repo
        self.decode_service = decode_service

    async def execute(self, token: str, profile_id: int, dto: UpdateProfileDTO):
        payload = await self.decode_service.decode_jwt_token(token)

        user_id = payload["user_id"]

        existing_profile = await self.profile_repo.get_profile_by_id(
            user_id, profile_id
        )

        if not existing_profile:
            return "Profile does not exist", 404

        await self.profile_repo.update_profile(existing_profile, **asdict(dto))

        return "Profile updated successfully", 200
