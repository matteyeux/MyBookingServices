from users.models.users import Users
from fastapi import APIRouter
from fastapi import HTTPException


router = APIRouter()


@router.get("/users/all", tags=["users"])
async def get_users():
    """Get all users"""
    users = Users().get_all_users()
    return {"users": users}


@router.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id: int = 1):
    """Get a user"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Can't use id <= 0")
    users = Users()
    user = users.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}
