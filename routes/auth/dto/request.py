from dataclasses import dataclass

@dataclass
class UserLoginRequest:
    email: str
    password: str