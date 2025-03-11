from dataclasses import dataclass


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
