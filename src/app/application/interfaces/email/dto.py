from dataclasses import dataclass


@dataclass
class SendEMailDTO:
    to_address: str
    code: int
