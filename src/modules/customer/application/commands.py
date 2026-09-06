from dataclasses import dataclass

from modules.customer.domain.customer import CustomerCreate


@dataclass(frozen=True)
class CustomerCreateCommand:
    payload: CustomerCreate


@dataclass(frozen=True)
class CustomerGetCommand:
    user_id: int

@dataclass(frozen=True)
class CustomerGetByEmailCommand:
    email: str
