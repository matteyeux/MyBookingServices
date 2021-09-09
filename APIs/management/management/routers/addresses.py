from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from management.models.addresses import Addresses
from management.utils import user_is_admin
from management.utils import user_logged
from pydantic import BaseModel


router = APIRouter()


class Address(BaseModel):
    hotel_id: Optional[int] = 1
    number: str
    street: str
    town: str
    postal_code: int


@router.get("/addresses/all/", tags=["addresses"])
async def get_all_addresses():
    """Get all addresses"""

    addresses = Addresses().get_all_addresses()
    return {"addresses": addresses}


@router.get("/addresses/{address_id}", tags=["addresses"])
async def get_address_by_id(address_id: int = 1):
    """Get detail about an address"""

    addresses = Addresses()
    address = addresses.get_address_by_id(address_id)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return {"address": address}


@router.get("/addresses/{hotel_id}", tags=["addresses"])
async def get_address_by_hotel_id(hotel_id: int = 1):
    """Get address by its hotel."""

    address = Addresses().get_address_by_hotel_id(hotel_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return {"address": address}


@router.get("/addresses/last/", tags=["addresses"])
async def get_last_address():
    """Get detail about an address"""

    addresses = Addresses().get_all_addresses()
    address = addresses[-1]
    return {"address": address}


@router.post("/addresses/", tags=["addresses"])
async def create_address(request: Request, address: Address):
    """Post detail about an address"""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    address = Addresses().create_address(address, address.hotel_id)
    return {"address": address}


@router.put("/addresses/{address_id}", tags=["addresses"])
async def update_address(
    request: Request,
    address: Address,
    address_id: int = 1,
):
    """Update address by its id."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    if not Addresses().get_address_by_id(address_id):
        raise HTTPException(status_code=404, detail="Address not found")

    address = Addresses().update_address(address, address_id)
    return {"address": address}


@router.delete("/addresses/{address_id}", tags=["addresses"])
async def delete_address(request: Request, address_id: int = 0):
    """Delete address by its id."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    if address_id > 0:
        address = Addresses().delete_address(address_id)

        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        return {}


# curl -X POST -d '{"key1":"value1", "key2":"value2"}' \
# 127.0.0.1:5555/addresses/test/
# @router.post("/addresses/test/", tags=["addresses"])
# async def test(request: Request):
#     return await request.json()
