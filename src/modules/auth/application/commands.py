from dataclasses import dataclass


@dataclass(frozen=True)
class EmailAuthenticationCommand:
    email: str
    raw_password: str  # bad: using raw customer password
