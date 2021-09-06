from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from management.models.rooms import Rooms
from management.utils import check_dates
from pydantic import BaseModel


router = APIRouter()


class Room(BaseModel):
    hotel_id: Optional[int] = 1
    room: str
    price: int
    capacity: int


@router.get("/rooms/all/", tags=["rooms"])
async def get_all_rooms(hotel_id: int = 0, capacity: int = 0):
    """Route to list all rooms."""

    rooms = Rooms()
    all_rooms = rooms.get_all_rooms(hotel_id, capacity)
    return {"rooms": all_rooms}


@router.get("/rooms/{room_id}", tags=["rooms"])
async def get_room_info_by_id(room_id: int = 0):
    """Get info about room"""

    if room_id <= 0:
        raise HTTPException(status_code=400, detail="Can't use id <= 0")
    rooms = Rooms()
    room = rooms.get_room_by_id(room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"room": room}


@router.get("/rooms/last/", tags=["rooms"])
async def get_last_room():
    """Route to list all rooms."""

    rooms = Rooms().get_all_rooms()
    last_room = rooms[-1]
    return {"room": last_room}


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


@router.post("/rooms", tags=["rooms"])
async def create_room(room: Room):
    """ Create a new room in a hotel. """

    room = Rooms().create_room(room)
    return {"room": room}


@router.put("/rooms/{room_id}", tags=["rooms"])
async def update_room(room: Room, room_id: int = 1):
    """ Update a room by its id. """

    if not Rooms().get_room_by_id(room_id):
        raise HTTPException(status_code=404, detail="Room not found")

    room = Rooms().update_room(room, room_id)
    return {"room": room}


@router.delete("/rooms/{room_id}", tags=["rooms"])
async def delete_room(room_id: int = 0):
    """ Delete a room by its id. """

    if room_id > 0:
        room = Rooms().delete_room(room_id)

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        return room
