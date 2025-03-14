from abc import ABC, abstractmethod


class IDecodeJWTToken(ABC):
    @abstractmethod
    def decode_jwt_token(self, token: str):
        pass

    @abstractmethod
    def check_is_admin(self, token: str):
        pass
