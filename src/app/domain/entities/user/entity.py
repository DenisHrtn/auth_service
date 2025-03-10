import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self

from app.domain.entities.user.exceptions import (
    InvalidUserEmailException,
    InvalidUserPasswordException,
    InvalidUserUsernameException,
)


@dataclass
class User:
    """
    Базовая реализация пользователя
    """

    id: int
    email: str
    username: str
    hashed_password: str
    code: int
    code_created_at: datetime
    is_admin: bool
    is_active: bool
    is_blocked: bool
    date_joined: datetime

    def __post_init__(self):
        self.code_created_at = datetime.now()
        self.date_joined = datetime.now()
        self.is_active = False
        self.is_blocked = False
        self.is_admin = False

    @staticmethod
    def validate_password(password: str) -> bool:
        """Проверка сложности пароля"""
        return (
            len(password) >= 8
            and bool(re.search(r"\d", password))
            and bool(re.search(r"[A-Z]", password))
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверка валидности email"""
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def validate_username(username: str) -> bool:
        """Проверка валидности username"""
        return len(username) >= 3

    @classmethod
    def register(cls, email: str, username: str, password: str) -> Self:
        """Метод регистрации пользователя"""
        if not cls.validate_password(password):
            raise InvalidUserPasswordException("Invalid password")
        if not cls.validate_email(email):
            raise InvalidUserEmailException("Invalid email")
        if not cls.validate_username(username):
            raise InvalidUserUsernameException("Invalid username")

        return cls(
            id=0,
            email=email,
            username=username,
            hashed_password=password,
            code=123456,
            code_created_at=datetime.now(),
            is_admin=False,
            is_active=False,
            is_blocked=False,
            date_joined=datetime.now(),
        )

    def is_password_expired(self, max_age_days: int) -> bool:
        """Проверка, истек ли срок действия пароля"""
        return self.code_created_at < datetime.now() - timedelta(days=max_age_days)
