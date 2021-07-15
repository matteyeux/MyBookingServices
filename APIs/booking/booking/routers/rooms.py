from booking.models.rooms import Rooms
from fastapi import APIRouter
from fastapi import HTTPException

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
async def get_all_rooms():
    """Get all rooms available
    for the moment we just grab all rooms.
    """
    rooms = Rooms()
    all_rooms = rooms.get_all_rooms()
    return {"rooms": all_rooms}
