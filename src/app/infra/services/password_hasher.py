from app.infra.security.password_hasher import hash_password


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return hash_password(password)
