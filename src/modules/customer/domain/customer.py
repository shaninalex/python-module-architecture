from dataclasses import dataclass
from datetime import datetime


@dataclass
class CustomerCreate:
    full_name: str
    email: str
    active: bool
    password: str


@dataclass
class CustomerUpdate:
    id: int
    full_name: str
    email: str


@dataclass
class Customer:
    id: int
    full_name: str
    email: str  # TODO: email field
    active: bool
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class CustomerCredential:
    id: int
    customer_id: int
    provider: str
    provider_user_id: str
    password_hash: str
    email: str
    created_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "provider": self.provider,
            "provider_user_id": self.provider_user_id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
