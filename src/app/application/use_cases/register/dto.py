from dataclasses import dataclass


@dataclass
class RegisterUserDTO:
    email: str
    username: str
    password: str
