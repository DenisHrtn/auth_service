from dataclasses import dataclass


@dataclass
class PermissionDto:
    id: int
    permission_name: str
    description: str
    tag: str


@dataclass
class UpdatePermissionDto:
    permission_name: str
    description: str
