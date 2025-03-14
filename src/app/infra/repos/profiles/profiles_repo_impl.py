from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.application.interfaces.unit_of_work.sql_base import IUnitOfWork
from app.application.use_cases.profiles.dto import map_profile_to_dto
from app.domain.interfaces.profiles.profiles_repo import ProfilesRepo
from app.infra.repos.sqla.models import Profile


class ProfilesRepoImpl(ProfilesRepo):
    def __init__(self, uow: IUnitOfWork):
        super().__init__(uow)

    async def get_profile_by_id(
        self, user_id: int, profile_id: str
    ) -> Optional[Profile]:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session

            result = await session_.execute(
                select(Profile).filter(
                    (Profile.id == profile_id) & (Profile.user_id == user_id)
                )
            )
            profile_model = result.scalars().first()

            if not profile_model:
                return None

            return profile_model

    async def get_all_profiles(self) -> list:
        async with self.uow(auto_commit=True):
            session_ = self.uow.session

            result = await session_.execute(
                select(Profile).options(joinedload(Profile.user))
            )

            profiles = result.scalars().all()

            return [map_profile_to_dto(profile) for profile in profiles]

    async def update_profile(self, profile_model, **kwargs):
        async with self.uow(auto_commit=True) as unit:
            session_ = unit.session

            profile_model = await session_.merge(profile_model)

            for key, value in kwargs.items():
                setattr(profile_model, key, value)

            await session_.flush()
            await session_.commit()
            await session_.refresh(profile_model)

            return "Successfully updated profile"
