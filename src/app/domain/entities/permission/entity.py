from dataclasses import dataclass


@dataclass
class Permission:
    """
    Базовая реализация роли
    """

    id: int
    permission_name: str
    description: str
    tag: str
