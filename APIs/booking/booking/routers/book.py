# from booking.models.book import Book
# from booking.models.rooms import Rooms
from fastapi import APIRouter
from fastapi import Request

# from fastapi import HTTPException


router = APIRouter()


# curl -X POST -d '{"key1":"value1", "key2":"value2"}' \
# 127.0.0.1:5555/hotels/test/
# @router.post("/hotels/test/", tags=["hotels"])
# async def test(request: Request):
#     return await request.json()


@router.post("/book/", tags=["book"])
async def book_room(request: Request):
    """Book room. Exepected parameters :
    - room_id
    - start_date
    - end_date
    - capacity
    - options
    """
    print(request.client.host)
    data = await request.json()
    print(data['key1'])
    print("here")
    # if room_id <= 0:
    #    raise HTTPException(status_code=400, detail="Can't use id <= 0")

    # check if room exists
    # rooms = Rooms()
    # room = rooms.get_room_by_id(room_id)
    # if not room:
    #    raise HTTPException(
    #        status_code=404,
    #        detail="Room not found",
    #    )

    # check if room is booked by looking at the table booking
    # for 2 dates (start and end).
    # booked_room = None  # Book().is_room_available()
    # if booked_room is True:
    #    raise HTTPException(
    #        status_code=403,
    #        detail="Room is already booked for this period",
    #    )
    return await request.json()  # {"room_id": room}
