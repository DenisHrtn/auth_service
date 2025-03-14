from abc import ABC, abstractmethod

from .dto import AuthTokenDTO, CreateJWTTokenDTO, VerifyPasswordDTO


class ILoginInterface(ABC):
    @abstractmethod
    async def verify_password(self, dto: VerifyPasswordDTO):
        pass

    @abstractmethod
    async def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    async def create_jwt_token(self, dto: CreateJWTTokenDTO) -> str:
        pass

    @abstractmethod
    async def create_access_token(self, dto: AuthTokenDTO) -> str:
        pass

    @abstractmethod
    async def create_refresh_token(self, dto: AuthTokenDTO) -> str:
        pass
