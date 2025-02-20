import random
import string
from datetime import datetime
from logging import getLogger

from .dto import UserDTO
from .exceptions import (
    UserWithInvalidPasswordException,
    UserWithoutEmailException,
    UserWithoutPasswordException,
)

loger = getLogger(__name__)


class User:
    """
    User entity class and provides methods for creating and updating users
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, dto: UserDTO) -> None:
        self.id = dto.id
        self.email = dto.email
        self.username = dto.username
        self.hashed_password = dto.hashed_password
        self.code = dto.code
        self.code_created_at = dto.code_created_at
        self.is_admin = dto.is_admin
        self.is_active = dto.is_active
        self.is_blocked = dto.is_blocked
        self.date_joined = dto.date_joined

    @staticmethod
    def generate_random_user_code(length: int = 6) -> str:
        """
        Generate random user code
        """

        return "".join(random.choices(string.digits, k=length))

    @classmethod
    def create(cls, email: str, username: str, hashed_password: str) -> "User":
        """
        Create a new user
        """

        return cls(
            dto=UserDTO(
                id=None,
                email=email,
                username=username,
                hashed_password=hashed_password,
                code=User.generate_random_user_code(),
                code_created_at=datetime.utcnow(),
                is_admin=False,
                is_active=True,
                is_blocked=False,
                date_joined=datetime.utcnow(),
            )
        )

    def update(self, **kwargs) -> None:
        """
        Update user attributes
        """

        allowed_fields = {
            "email",
            "username",
            "hashed_password",
            "is_admin",
            "is_active",
            "is_blocked",
        }

        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)

    def block(self) -> None:
        self.is_blocked = True
        self.is_active = False

    def unblock(self) -> None:
        self.is_blocked = False
        self.is_active = True

    @staticmethod
    def _check_email(email: str) -> None:
        if not email:
            raise UserWithoutEmailException

    @staticmethod
    def _check_hashed_password(password: str) -> None:
        if not password:
            raise UserWithoutPasswordException
        if len(password) < 8:
            raise UserWithInvalidPasswordException
