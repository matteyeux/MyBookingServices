# from booking.database import Database
from fastapi import APIRouter


router = APIRouter()


@router.post("/book/{room_id}", tags=["book"])
async def book_room(room_id: int = 0):
    """Book room"""
    if room_id <= 0:
        return None

    return {"room_id": room_id}


@router.get("/book/all/", tags=["book"])
async def booked_rooms():
    """Get all booked rooms."""
    return {"booked_rooms": "booked_rooms"}
