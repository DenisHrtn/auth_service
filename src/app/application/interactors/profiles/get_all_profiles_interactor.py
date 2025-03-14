from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.profiles.get_all_profiles_with_users import (
    GetAllProfilesWithUsersUseCase,
)
from app.domain.interfaces.profiles.profiles_repo import ProfilesRepo


class GetAllProfilesInteractor(GetAllProfilesWithUsersUseCase):
    def __init__(self, uow: IUnitOfWork, profile_repo: ProfilesRepo):
        self.uow = uow
        self.profile_repo = profile_repo

    async def get_all_profiles_with_users(self):
        profiles = await self.profile_repo.get_all_profiles()

        return profiles
