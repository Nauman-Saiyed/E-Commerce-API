from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.schemas.orders import OrderCreate, OrderStatusUpdate
from app.core.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

ALLOWED_STATUSES = {"pending", "confirmed", "shipped", "delivered", "cancelled"}

@router.post("/place", status_code=status.HTTP_201_CREATED)
async def place_order(
    data: OrderCreate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    if data.qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    # Validate product
    product = await db.products.find_one(
        {"_id": ObjectId(data.product_id), "deleted_at": None}
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 🔐 Price always from DB
    price = product["price"]

    order = {
        "_id": ObjectId(),
        "user_id": ObjectId(user_id),
        "product_id": ObjectId(data.product_id),
        "price": price,
        "qty": data.qty,
        "total": price * data.qty,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "deleted_at": None,
    }

    await db.orders.insert_one(order)
    return {"message": "Order placed successfully"}


@router.get("/my-orders")
async def get_my_orders(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    orders = []
    async for o in db.orders.find(
        {"user_id": ObjectId(user_id), "deleted_at": None}
    ):
        orders.append({
            "id": str(o["_id"]),
            "product_id": str(o["product_id"]),
            "price": o["price"],
            "qty": o["qty"],
            "total": o["total"],
            "status": o["status"],
            "created_at": o["created_at"],
        })
    return orders

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id), "deleted_at": None},
        {
            "$set": {
                "status": data.status.value,  # Enum → string
                "updated_at": datetime.utcnow(),
            }
        },
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order status updated successfully"}

