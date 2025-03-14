from abc import ABC, abstractmethod


class GetAllRolesUseCase(ABC):
    @abstractmethod
    async def get_all_roles(self, token: str):
        pass
