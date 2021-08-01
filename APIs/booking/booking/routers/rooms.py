from booking.models.rooms import Rooms
from fastapi import APIRouter
from fastapi import HTTPException

# from fastapi import Request

router = APIRouter()


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


@router.get("/rooms/all/", tags=["rooms"])
async def get_all_rooms(
    hotel_id: int = 1,
    capacity: int = 1,
    start_date: str = None,
    end_date: str = None,
):
    """Get available rooms by hotel.
    Optionaly you set by start and end date and capacity
    """
    # rooms = Rooms()
    all_rooms = None
    return {"rooms": all_rooms}


# @router.get("/rooms/test/")
# async def do_test(param1: str, param2: str):
# #async def do_test(request: Request):
#     print(param2)
#     return {"test"}
#     #return await request.json()
