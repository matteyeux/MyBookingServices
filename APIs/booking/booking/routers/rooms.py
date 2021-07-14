from booking.database import Database
from fastapi import APIRouter


router = APIRouter()


@router.get("/rooms/{room_id}", tags=["rooms"])
async def get_room_info_by_id(room_id: int = 0):
    """Get info about room"""
    if room_id <= 0:
        return None
    db = Database(
        user="root", password="root",
        host="localhost", database="mydb",
    )
    return {"room_id": db.get_room_by_id(room_id)}


@router.get("/rooms/all/", tags=["rooms"])
async def get_all_rooms():
    """Book rooms available.
    for the moment we just grab all rooms.
    """
    db = Database(
        user="root", password="root",
        host="localhost", database="mydb",
    )
    return {"rooms": db.get_rooms()}
