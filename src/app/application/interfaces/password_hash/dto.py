from dataclasses import dataclass


@dataclass
class PasswordHashDTO:
    password: str
