import datetime
import random
from dataclasses import dataclass, field
from typing import List


def random_product_image() -> str:
    """Make url for random shoes image from src/adapters/web/static/images """
    return f"images/sneakers-{random.randint(1, 9)}.webp"


@dataclass
class ProductVariantModel:
    id: int
    title: str
    description: str
    sku: str
    barcode: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "sku": self.sku,
            "barcode": self.barcode,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class ProductModel:
    id: int
    title: str
    description: str
    short_description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    variants: List[ProductVariantModel]

    # NOTE:
    # until I add images in schema - this will be image field
    image: str = field(default_factory=random_product_image)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "short_description": self.short_description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "variants": [v.to_dict() for v in self.variants]
        }
