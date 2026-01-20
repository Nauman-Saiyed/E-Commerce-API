from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateCategory(BaseModel):
    name : str
    # slug : str


class UpdateCategory(BaseModel):
    name : Optional[str] = None
    # slug : Optional[str] = None


class CategoryResponse(BaseModel):
    category_id : str
    name : str
    slug : str
    created_at : datetime