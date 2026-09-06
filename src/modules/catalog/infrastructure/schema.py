import datetime

from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from modules.catalog.domain.product import ProductModel


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    short_description: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Product(id={self.id!r} title={self.title!r})"

    def to_model(self) -> ProductModel:
        return ProductModel(
            id=self.id,
            title=self.title,
            description=self.description,
            short_description=self.short_description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
