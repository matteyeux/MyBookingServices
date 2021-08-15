from management.models.hotels import Hotels
from fastapi import APIRouter

# from fastapi import Request

router = APIRouter()


@router.get("/hotels/all/", tags=["hotels"])
async def get_hotels():
    """Get all hotels"""
    hotels = Hotels().get_all_hotels()
    return {"hotels": hotels}


@router.get("/hotels/{hotel_id}", tags=["hotels"])
async def get_hotel_by_id(hotel_id: int = 1):
    """Get detail about an hotel"""
    hotels = Hotels()
    hotel = hotels.get_hotel_by_id(hotel_id)
    return {"hotel": hotel}


@router.post("/hotels/", tags=["hotels"])
async def post_hotel():
    """Post detail about an hotel"""
    hotels = Hotels()
    hotel = hotels.get_hotel_by_id()
    return {"hotel": hotel}


# curl -X POST -d '{"key1":"value1", "key2":"value2"}' \
# 127.0.0.1:5555/hotels/test/
# @router.post("/hotels/test/", tags=["hotels"])
# async def test(request: Request):
#     return await request.json()
