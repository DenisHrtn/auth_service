import re
from datetime import datetime, timedelta

from app.domain.entities.user.dto import UserDTO
from app.domain.entities.user.exceptions import (
    InvalidUserEmailException,
    InvalidUserPasswordException,
    InvalidUserUsernameException,
)


class User:
    """
    Базовая реализация пользователя
    """

    def __init__(self, data: UserDTO) -> None:
        self.id = data.id
        self.email = data.email
        self.username = data.username
        self.hashed_password = data.hashed_password
        self.code = data.code
        self.code_created_at = data.code_created_at
        self.is_admin = data.is_admin
        self.is_active = data.is_active
        self.is_blocked = data.is_blocked
        self.date_joined = data.date_joined

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Проверка сложности пароля
        """

        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Проверка валидности email
        """

        if not re.search(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True

    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Проверка валидности username
        """

        if len(username) < 3:
            return False
        return True

    @classmethod
    def register(
        cls,
        email: str,
        username: str,
        password: str,
    ) -> "User":
        """
        Метод регистрации пользователя
        """

        if not cls.validate_password(password):
            raise InvalidUserPasswordException("Invalid password")

        if not cls.validate_email(email):
            raise InvalidUserEmailException("Invalid email")

        if not cls.validate_username(username):
            raise InvalidUserUsernameException("Invalid username")

        user_dto = UserDTO(
            id=0,
            email=email,
            username=username,
            hashed_password=password,
            code=123456,
            code_created_at=datetime.utcnow(),
            is_admin=False,
            is_active=False,
            is_blocked=False,
            date_joined=datetime.utcnow(),
        )
        return cls(user_dto)

    def activate(self) -> None:
        """
        Активация пользователя
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Деактивация пользователя
        """

        self.is_active = False

    def block(self) -> None:
        """
        Блокировка пользователя
        """

        self.is_blocked = True
        self.is_active = False

    def unblock(self) -> None:
        """
        Разблокировка пользователя
        """

        self.is_blocked = False
        self.is_active = True

    def is_password_expired(self, max_age_days: int) -> bool:
        """
        Проверка, истек ли срок действия пароля
        """
        if self.code_created_at < datetime.utcnow() - timedelta(days=max_age_days):
            return True
        return False
