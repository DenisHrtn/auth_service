from dataclasses import dataclass

from .exceptions import InvalidRoleNameException


@dataclass
class Role:
    """
    Базовая реализация роли
    """

    id: int
    role_name: str
    description: str
    permissions: list[int]
    user_id: int

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []

    @staticmethod
    def validate_role_name(role_name: str) -> bool:
        """
        Проверка имени роли
        """

        return len(role_name) > 5

    @classmethod
    def create(
        cls, role_name: str, description: str, permissions: list[int], user_id: int
    ):
        """
        Метод создания роли
        """

        if not cls.validate_role_name(role_name):
            raise InvalidRoleNameException("Invalid role name")

        return cls(
            id=0,
            role_name=role_name,
            description=description,
            permissions=permissions,
            user_id=user_id,
        )
