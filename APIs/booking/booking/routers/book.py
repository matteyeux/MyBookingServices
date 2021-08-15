from booking.models.book import Book
from booking.models.rooms import Rooms
from fastapi import APIRouter
from fastapi import HTTPException


router = APIRouter()


@router.post("/book/{room_id}", tags=["book"])
async def book_room(room_id: int = 0):
    """Book room"""
    if room_id <= 0:
        raise HTTPException(status_code=400, detail="Can't use id <= 0")

    # check if room exists
    room = Rooms().get_room_by_id(room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found, can't book it.",
        )

    # currently we only check if the room is booked, what ever the date
    if room[0]['booked'] is True:
        raise HTTPException(
            status_code=403,
            detail="Room is already booked for this period",
        )
    return {"room_id": room}


@router.get("/book/all", tags=["book"])
async def available_rooms():
    """Get available rooms to book."""
    available_rooms = Book().get_available_rooms()
    return {"available_rooms": available_rooms}
