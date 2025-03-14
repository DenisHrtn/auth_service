from abc import ABC, abstractmethod

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork


class ProfilesRepo(ABC):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    @abstractmethod
    async def get_profile_by_id(self, user_id: int, profile_id: int):
        pass

    @abstractmethod
    async def get_all_profiles(self, offset: int, limit: int):
        pass

    @abstractmethod
    async def update_profile(self, profile_model, **kwargs):
        pass
