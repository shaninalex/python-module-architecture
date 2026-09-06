from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from bootstrap.database import Base


class CustomerLoginHistoryORM(Base):
    __tablename__ = "customers_login_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    logged_in_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
