from users.models.users import Users
from fastapi import APIRouter


router = APIRouter()


@router.get("/users/all/", tags=["users"])
async def get_users():
    """Get all users"""
    users = Users().get_all_users()
    return {"users": users}


@router.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id: int = 1):
    """Get a user"""
    users = Users()
    user = users.get_user_by_id(user_id)
    return {"user": user}
