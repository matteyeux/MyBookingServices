from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from management.models.addresses import Addresses
from management.models.hotels import Hotels
from management.utils import user_is_admin
from management.utils import user_logged
from pydantic import BaseModel

# from fastapi import Request

router = APIRouter()


class Hotel(BaseModel):
    name: str
    telephone: str
    website: str
    description: Optional[str] = None
    owner: str


class Address(BaseModel):
    number: str
    street: str
    town: str
    postal_code: str


@router.get("/hotels/all/", tags=["hotels"])
async def get_all_hotels():
    """Get all hotels"""

    hotels = Hotels().get_all_hotels()
    return {"hotels": hotels}


@router.get("/hotels/{hotel_id}", tags=["hotels"])
async def get_hotel_by_id(hotel_id: int = 1):
    """Get detail about an hotel"""

    hotels = Hotels()
    hotel = hotels.get_hotel_by_id(hotel_id)

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return {"hotel": hotel}


@router.get("/hotels/last/", tags=["hotels"])
async def get_last_hotel():
    """Get detail about an hotel"""

    hotels = Hotels().get_all_hotels()
    hotel = hotels[-1]
    return {"hotel": hotel}


@router.post("/hotels/", tags=["hotels"])
async def create_hotel(request: Request, hotel: Hotel, address: Address):
    """Post detail about an hotel"""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    hotels = Hotels()
    hotel = hotels.create_hotel(hotel)

    address = Addresses().create_address(address, hotel["id"])
    hotel = hotels.get_hotel_by_id(hotel["id"])
    return {"hotel": hotel}


@router.put("/hotels/{hotel_id}", tags=["hotels"])
async def update_hotel(request: Request, hotel: Hotel, hotel_id: int = 1):
    """Update hotel by its id."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    if not Hotels().get_hotel_by_id(hotel_id):
        raise HTTPException(status_code=404, detail="Hotel not found")

    hotel = Hotels().update_hotel(hotel, hotel_id)
    return {"hotel": hotel}


@router.delete("/hotels/{hotel_id}", tags=["hotels"])
async def delete_hotel(request: Request, hotel_id: int = 0):
    """Delete hotel by its id."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    if hotel_id > 0:
        addresses = Addresses().get_address_by_hotel_id(hotel_id)

        if len(addresses) == 0:
            raise HTTPException(
                status_code=404,
                detail="No address for this hotel",
            )

        address_id = addresses[0].id
        Addresses().delete_address(address_id)

        hotel = Hotels().delete_hotel(hotel_id)

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        return {}


# curl -X POST -d '{"key1":"value1", "key2":"value2"}' \
# 127.0.0.1:5555/hotels/test/
# @router.post("/hotels/test/", tags=["hotels"])
# async def test(request: Request):
#     return await request.json()
