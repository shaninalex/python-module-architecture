from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bootstrap.database import Base
from modules.customer.domain.customer import Customer, CustomerCredential


class CustomerORM(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    active: Mapped[bool] = mapped_column(Boolean())

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    credentials: Mapped[List["CustomerCredentialsORM"]] = relationship(back_populates="customer",
                                                                       cascade="all, delete-orphan")

    def to_model(self) -> Customer:
        return Customer(
            id=self.id,
            full_name=self.full_name,
            email=self.email,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class CustomerCredentialsORM(Base):
    __tablename__ = "customers_credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String())
    provider_user_id: Mapped[str] = mapped_column(String())
    password_hash: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["CustomerORM"] = relationship(back_populates="credentials")

    def to_model(self) -> CustomerCredential:
        return CustomerCredential(
            id=self.id,
            provider=self.provider,
            provider_user_id=self.provider_user_id,
            password_hash=self.password_hash,
            email=self.email,
            created_at=self.created_at,
            customer_id=self.customer_id,
        )
