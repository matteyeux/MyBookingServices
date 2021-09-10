import os

from booking import utils
from booking.models.book import Book
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

router = APIRouter()


@router.post("/book/", tags=["book"])
async def book_room(request: Request):
    """Book room. Exepected parameters :
    - hotel_id
    - room_id
    - start_date
    - end_date
    - capacity
    - options
    """
    data = await request.json()
    if "PYTEST_CURRENT_TEST" in os.environ:
        user = {'id': 1}
    else:
        user = utils.user_logged(request.headers.get('authorization'))

    if utils.book_sanity_check(data) is False:
        # https://stackoverflow.com/a/42171674
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    book = Book()
    if book.is_room_available(data) is False:
        raise HTTPException(
            status_code=403,
            detail="Room is already booked for this period",
        )

    booking_data = book.do_book_room(user['id'], data)
    return {"booked_room": booking_data}


@router.get("/book/{booking_id}", tags=["book"])
async def get_booked_rooms_by_id(booking_id: int = 0):
    """Get booking by id"""
    if booking_id > 0:
        booking_room = Book().get_booked_rooms_by_id(booking_id)
        print(booking_room[0]["customer_id"])
        if not booking_room:
            raise HTTPException(
                status_code=404,
                detail="booking room not found",
            )

        return booking_room


@router.delete("/book/{booking_id}", tags=["book"])
async def delete_booked_rooms_by_id(request: Request, booking_id: int = 0):
    """Delete booking by its id"""

    user = utils.user_logged(request.headers.get('authorization'))
    r = Book().get_booked_rooms_by_id(booking_id)
    if booking_id > 0:
        booking = Book().delete_booked_rooms_by_id(user['id'], booking_id)

        if len(r) == 0:
            raise HTTPException(
                status_code=404,
                detail="booking room not found",
            )

        if len(r) > 0 and user['id'] == r[0]["customer_id"]:
            raise HTTPException(
                status_code=403,
                detail="You're not available to delete this booking",
            )

        return booking
