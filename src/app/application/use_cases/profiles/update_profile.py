from abc import ABC, abstractmethod

from .dto import UpdateProfileDTO


class UpdateProfileUseCase(ABC):
    @abstractmethod
    async def execute(self, token: str, profile_id: int, dto: UpdateProfileDTO):
        pass
