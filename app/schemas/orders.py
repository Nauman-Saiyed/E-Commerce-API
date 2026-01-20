from pydantic import BaseModel
from datetime import datetime , UTC
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    product_id: str
    qty: int


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: str
    user_id: str
    product_id: str
    price: float
    qty: int
    total: float
    status: OrderStatus
    created_at: datetime
