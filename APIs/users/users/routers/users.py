from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from users.models.auth import UserLoginSchema
from users.models.auth import UserSignupSchema
from users.models.users import Users
from users.utils.auth_bearer import JWTBearer
from users.utils.auth_handler import decodeJWT
from users.utils.auth_handler import signJWT


router = APIRouter()


@router.get("/users/all", tags=["users"])
async def get_users():
    """Get all users"""
    users = Users().get_all_users()
    result = []
    for user in users:
        user_clean = {
            "id": user["id"],
            "role": user["role"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "telephone": user["telephone"],
        }
        result.append(
            user_clean,
        )
    return {"users": result}


@router.get("/users/me", dependencies=[Depends(JWTBearer())], tags=["users"])
async def get_connected_user(request: Request):
    """Get connected users"""
    bearer = request.headers.get('authorization').replace("Bearer ", "")
    result = decodeJWT(bearer)
    users = Users()
    user = users.get_user_by_mail(result["email"])
    return {
        "id": user["id"],
        "role": user["role"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "telephone": user["telephone"],
    }


@router.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id: int = 1):
    """Get a user"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Can't use id <= 0")
    users = Users()
    user = users.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user["id"],
        "role": user["role"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "telephone": user["telephone"],
    }


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
