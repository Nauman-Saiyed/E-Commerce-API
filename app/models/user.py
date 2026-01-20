from datetime import datetime , UTC
from bson import ObjectId
from app.core.security import hash_password

def user_detail(data : dict):
    return {
        "_id" : ObjectId(),
        "name" : data["name"],
        "email" : data["email"],
        "phone" : data["phone"],
        "password" : hash_password(data["password"]),
        "created_at" : datetime.now(UTC),
        "updated_at" : datetime.now(UTC),
        "deleted_at" : None
    }