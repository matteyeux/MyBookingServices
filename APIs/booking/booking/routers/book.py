from booking import utils
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

# from booking.models.book import Book


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
    data = await request.json()

    if utils.book_sanity_check(data) is False:
        # https://stackoverflow.com/a/42171674
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    # check if room is available at the said date
    # if is_room_available(...) is False:
    #     raise HTTPException(
    #         status_code=403, detail="Room is already booked for this period"
    #     )

    # book = Book()
    # booking = book.do_book_room(data)
    # book_room

    return {"room": data}
