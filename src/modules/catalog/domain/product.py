import datetime
from dataclasses import dataclass

@dataclass
class ProductModel:
    id: int
    title: str
    description: str
    short_description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
