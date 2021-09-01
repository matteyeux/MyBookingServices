from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from users.models.auth import UserLoginSchema
from users.models.auth import UserSignupSchema
from users.models.users import Users
from users.utils.auth_handler import signJWT


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


@router.post("/users/signup", tags=["users"])
async def create_user(user: UserSignupSchema = Body(...)):
    users = Users()
    users.create_user(user)
    return signJWT("USER", user.email)


@router.post("/users/login", tags=["users"])
async def user_login(user: UserLoginSchema = Body(...)):
    users = Users()
    user_db = users.check_user_login(user.email, user.password)
    if user_db is not None:
        return signJWT(user_db.role, user_db.email)
    else:
        return {
            "details": "Bad email or password",
        }
