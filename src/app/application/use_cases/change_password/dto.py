from dataclasses import dataclass


@dataclass
class ChangePasswordDto:
    code: int
    password: str
    password_again: str
