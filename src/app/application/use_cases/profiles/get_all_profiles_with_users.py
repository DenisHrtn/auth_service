from abc import ABC, abstractmethod


class GetAllProfilesWithUsersUseCase(ABC):
    @abstractmethod
    async def get_all_profiles_with_users(self):
        pass
