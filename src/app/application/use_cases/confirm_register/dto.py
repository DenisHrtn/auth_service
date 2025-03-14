from dataclasses import dataclass


@dataclass
class ConfirmRegisterDTO:
    email: str
    code: int
