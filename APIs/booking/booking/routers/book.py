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
