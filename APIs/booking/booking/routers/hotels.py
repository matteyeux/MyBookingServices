from booking.models.hotels import Hotels
from fastapi import APIRouter

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
