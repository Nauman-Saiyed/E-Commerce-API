from fastapi import Depends, HTTPException, status, APIRouter
from bson import ObjectId
from datetime import datetime, UTC
from slugify import slugify
from app.schemas.category import CreateCategory, UpdateCategory
from app.core.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["Category"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CreateCategory,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    slug = slugify(data.name)

    existing = await db.categories.find_one(
        {"slug": slug, "deleted_at": None}
    )
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = {
        "_id": ObjectId(),
        "name": data.name,
        "slug": slug,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "deleted_at": None,
    }

    await db.categories.insert_one(category)
    return {"message": "Category created successfully"}


@router.get("")
async def get_categories(db=Depends(get_db)):
    categories = []

    async for cat in db.categories.find({"deleted_at": None}):
        categories.append({
            "category_id": str(cat["_id"]),
            "name": cat["name"],
            "slug": cat["slug"],
            "created_at": cat["created_at"],
        })

    return categories


@router.get("/{category_id}")
async def get_one_category(category_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")

    category = await db.categories.find_one(
        {"_id": ObjectId(category_id), "deleted_at": None}
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return {
        "category_id": str(category["_id"]),
        "name": category["name"],
        "slug": category["slug"],
        "created_at": category["created_at"],
    }

@router.put("/{category_id}")
async def update_category(
    category_id: str,
    data: UpdateCategory,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if "name" in update_data:
        update_data["slug"] = slugify(update_data["name"])

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    update_data["updated_at"] = datetime.now(UTC)

    result = await db.categories.update_one(
        {"_id": ObjectId(category_id), "deleted_at": None},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category updated successfully"}

@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    db=Depends(get_db),
    _: str = Depends(get_current_user),
):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")

    result = await db.categories.update_one(
        {"_id": ObjectId(category_id), "deleted_at": None},
        {"$set": {"deleted_at": datetime.now(UTC)}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted successfully"}

