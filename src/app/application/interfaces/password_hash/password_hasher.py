from abc import ABC, abstractmethod

from .dto import PasswordHashDTO


class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, dto: PasswordHashDTO) -> str:
        pass
