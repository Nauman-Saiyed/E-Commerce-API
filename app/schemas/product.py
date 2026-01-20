from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CreateProduct(BaseModel):
    name: str
    price: float = Field(gt=0)
    category_id: str
    tags: Optional[List[str]] = []


class UpdateProduct(BaseModel):
    name: Optional[str]
    price: Optional[float] = Field(default=None, gt=0)
    category_id: Optional[str]
    tags: Optional[List[str]]


class ProductResponse(BaseModel):
    product_id: str
    name: str
    slug: str
    price: float
    category_id: str
    tags: List[str]
    created_at: datetime
