from booking.models.rooms import Rooms
from booking.utils import check_dates
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.get("/rooms/all/", tags=["rooms"])
async def get_all_rooms(hotel_id: int = 0, capacity: int = 0):
    """Route to list all rooms."""
    rooms = Rooms()
    all_rooms = rooms.get_all_rooms(hotel_id, capacity)

    return {"rooms": all_rooms}


@router.get("/rooms/all/available/", tags=["rooms"])
async def get_available_rooms(
    hotel_id: int = 1,
    capacity: int = 0,
    start_date: str = None,
    end_date: str = None,
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
        capacity,
        start_date,
        end_date,
    )

    if available_rooms is None:
        raise HTTPException(
            status_code=500,
            detail="Service Unavailable",
        )

    return {"rooms": available_rooms}


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


@router.get("/rooms/options/", tags=["rooms"])
async def get_options():
    """Route to list all rooms."""
    rooms = Rooms()
    all_options = rooms.get_all_options()

    return {"options": all_options}
