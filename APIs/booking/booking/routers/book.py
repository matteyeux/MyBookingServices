from booking.models.book import Book
from booking.models.rooms import Rooms
from fastapi import APIRouter
from fastapi import HTTPException

# from fastapi import Request


router = APIRouter()


@router.post("/book/{room_id}", tags=["book"])
async def book_room(room_id: int = 1):
    """Book room"""
    if room_id <= 0:
        raise HTTPException(status_code=400, detail="Can't use id <= 0")

    # check if room exists
    rooms = Rooms()
    room = rooms.get_room_by_id(room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    # check if room is booked by looking at the table booking
    # for 2 dates (start and end).
    booked_room = Book().is_room_available()
    if booked_room is True:
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
