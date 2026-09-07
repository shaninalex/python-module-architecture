import datetime
from typing import List

from sqlalchemy import String, func, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bootstrap.database import Base
from modules.catalog.domain.product import Product, ProductVariant


class ProductVariantORM(Base):
    __tablename__ = "product_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    sku: Mapped[str] = mapped_column(String())
    barcode: Mapped[str] = mapped_column(String())
    image_url: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["ProductORM"] = relationship(back_populates="variants")
    images: Mapped[List["ProductVariantImageORM"]] = relationship(back_populates="variant",
                                                                  cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ProductVariant(id={self.id!r} title={self.title!r})"

    def to_model(self) -> ProductVariant:
        return ProductVariant(
            id=self.id,
            title=self.title,
            description=self.description,
            sku=self.sku,
            barcode=self.barcode,
            image_url=self.image_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class ProductORM(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    short_description: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    image_url: Mapped[str] = mapped_column(String())
    variants: Mapped[List["ProductVariantORM"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Product(id={self.id!r} title={self.title!r})"

    def to_model(self) -> Product:
        return Product(
            id=self.id,
            title=self.title,
            description=self.description,
            short_description=self.short_description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            image_url=self.image_url,
            variants=[d.to_model() for d in self.variants],
        )


class ProductVariantImageORM(Base):
    __tablename__ = "product_product_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("product_variants.id"))
    alt: Mapped[str] = mapped_column(String())
    position: Mapped[int] = mapped_column(Integer())
    image_url: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    variant: Mapped["ProductVariantORM"] = relationship(back_populates="images")

    def __repr__(self) -> str:
        return f"ProductVariantImage(id={self.id!r} title={self.variant_id!r})"
