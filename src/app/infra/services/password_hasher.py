from app.application.interfaces.password_hash.dto import PasswordHashDTO
from app.application.interfaces.password_hash.password_hasher import IPasswordHasher
from app.infra.security.hash_password import hash_password


class PasswordHasher(IPasswordHasher):
    def hash_password(self, dto: PasswordHashDTO) -> str:
        return hash_password(dto.password)
