from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from datetime import datetime, UTC
from slugify import slugify

from app.schemas.product import CreateProduct, UpdateProduct
from app.core.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    data: CreateProduct,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    if not ObjectId.is_valid(data.category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")

    category = await db.categories.find_one(
        {"_id": ObjectId(data.category_id), "deleted_at": None}
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    slug = slugify(data.name)

    existing = await db.products.find_one(
        {"slug": slug, "deleted_at": None}
    )
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    product = {
        "_id": ObjectId(),
        "name": data.name,
        "slug": slug,
        "price": data.price,
        "category_id": ObjectId(data.category_id),
        "tags": data.tags or [],
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "deleted_at": None,
    }

    await db.products.insert_one(product)
    return {"message": "Product created successfully"}

@router.get("")
async def get_products(db=Depends(get_db)):
    products = []

    async for p in db.products.find({"deleted_at": None}):
        products.append({
            "product_id": str(p["_id"]),
            "name": p["name"],
            "slug": p["slug"],
            "price": p["price"],
            "category_id": str(p["category_id"]),
            "tags": p["tags"],
            "created_at": p["created_at"],
        })

    return products

@router.get("/{product_id}")
async def get_product(product_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product id")

    product = await db.products.find_one(
        {"_id": ObjectId(product_id), "deleted_at": None}
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product_id": str(product["_id"]),
        "name": product["name"],
        "slug": product["slug"],
        "price": product["price"],
        "category_id": str(product["category_id"]),
        "tags": product["tags"],
        "created_at": product["created_at"],
    }

@router.put("/{product_id}")
async def update_product(
    product_id: str,
    data: UpdateProduct,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product id")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if "category_id" in update_data:
        if not ObjectId.is_valid(update_data["category_id"]):
            raise HTTPException(status_code=400, detail="Invalid category id")

        category = await db.categories.find_one(
            {"_id": ObjectId(update_data["category_id"]), "deleted_at": None}
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data["category_id"] = ObjectId(update_data["category_id"])

    if "name" in update_data:
        update_data["slug"] = slugify(update_data["name"])

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    update_data["updated_at"] = datetime.now(UTC)

    result = await db.products.update_one(
        {"_id": ObjectId(product_id), "deleted_at": None},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product updated successfully"}

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product id")

    result = await db.products.update_one(
        {"_id": ObjectId(product_id), "deleted_at": None},
        {"$set": {"deleted_at": datetime.now(UTC)}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}
