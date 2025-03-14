from abc import ABC, abstractmethod


class GetAllPermissionsUseCase(ABC):
    @abstractmethod
    async def get_all_permissions(self, token: str):
        pass
