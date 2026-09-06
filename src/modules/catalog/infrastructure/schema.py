import datetime
from typing import List

from sqlalchemy import String, func, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from modules.catalog.domain.product import ProductModel, ProductVariantModel


class Base(DeclarativeBase):
    pass


class ProductVariant(Base):
    __tablename__ = "product_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    sku: Mapped[str] = mapped_column(String())
    barcode: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="variants")

    def __repr__(self) -> str:
        return f"ProductVariant(id={self.id!r} title={self.title!r})"

    def to_model(self) -> ProductVariantModel:
        return ProductVariantModel(
            id=self.id,
            title=self.title,
            description=self.description,
            sku=self.sku,
            barcode=self.barcode,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    short_description: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    variants: Mapped[List["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Product(id={self.id!r} title={self.title!r})"

    def to_model(self) -> ProductModel:
        return ProductModel(
            id=self.id,
            title=self.title,
            description=self.description,
            short_description=self.short_description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            variants=[d.to_model() for d in self.variants],
        )
