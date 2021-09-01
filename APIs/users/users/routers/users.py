from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from users.auth.auth_handler import signJWT
from users.model import UserLoginSchema
from users.model import UserSchema
from users.models.users import Users


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


users = []


@router.post("/users/signup", tags=["users"])
async def create_user(user: UserSchema = Body(...)):
    # replace with db call, making sure to hash the password first
    users.append(user)
    return signJWT(user.email)


@router.post("/users/login", tags=["users"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!",
    }


# TODO: Move this function to as service that call the db
def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False
