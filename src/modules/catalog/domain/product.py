import datetime
import random
from dataclasses import dataclass, field


def random_product_image() -> str:
    """Make url for random shoes image from src/adapters/web/static/images """
    return f"images/sneakers-{random.randint(1, 9)}.webp"


@dataclass
class ProductModel:
    id: int
    title: str
    description: str
    short_description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    # NOTE:
    # until I add images in schema - this will be image field
    image: str = field(default_factory=random_product_image)
