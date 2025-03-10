from dataclasses import dataclass


@dataclass
class SendCodeAgainDTO:
    email: str


@dataclass
class SendCodeAgainOutputDTO:
    email: str
    code: int
