from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from management.models.rooms import Rooms
from management.utils import check_dates
from utils import user_is_admin
from utils import user_logged

router = APIRouter()


@router.get("/rooms/test-user", tags=["users"])
async def get_connected_user(request: Request):
    user = user_logged(request.headers.get('authorization'))
    return user


@router.get("/rooms/test-admin", tags=["users"])
async def get_check_user_is_admin(request: Request):
    user = user_logged(request.headers.get('authorization'))
    return user_is_admin(user)


@router.get("/rooms/{room_id}", tags=["rooms"])
async def get_room_info_by_id(room_id: int = 0):
    """Get info about room"""
    if room_id <= 0:
        raise HTTPException(status_code=400, detail="Can't use id <= 0")
    rooms = Rooms()
    room = rooms.get_room_by_id(room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"room_id": room}


# @router.get("/rooms/test/")
# async def do_test(param1: str, param2: str):
# #async def do_test(request: Request):
#     print(param2)
#     return {"test"}
#     #return await request.json()


@router.get("/rooms/all/available/", tags=["rooms"])
async def get_available_rooms(
    hotel_id: int = 1,
    start_date: str = None,
    end_date: str = None,
    capacity: int = 0,
):
    """Route to get available rooms."""
    if check_dates(start_date, end_date) is False:
        raise HTTPException(
            status_code=400,
            detail="Specified dates are invalid",
        )

    rooms = Rooms()

    available_rooms = rooms.get_available_rooms(
        hotel_id,
        start_date,
        end_date,
        capacity,
    )
    return {"rooms": available_rooms}


@router.get("/rooms/all/", tags=["rooms"])
async def get_all_rooms(hotel_id: int = 0, capacity: int = 0):
    """Route to list all rooms."""
    rooms = Rooms()
    all_rooms = rooms.get_all_rooms(hotel_id, capacity)

    return {"rooms": all_rooms}
