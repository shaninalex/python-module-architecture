from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationData:
    customer_id: int
    password_hash: str
    active: bool