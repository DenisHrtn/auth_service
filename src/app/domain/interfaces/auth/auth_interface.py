from abc import ABC, abstractmethod
from typing import Optional


class IAuthInterface(ABC):
    @abstractmethod
    async def put_token_in_redis(self, token: str) -> str:
        pass

    @abstractmethod
    async def validate_token(self, token: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def deactivate_token(self, token: str) -> None:
        pass
