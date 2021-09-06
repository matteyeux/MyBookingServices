from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from management.models.addresses import Addresses
from pydantic import BaseModel


router = APIRouter()


class Address(BaseModel):
    hotel_id: Optional[int] = 1
    number: str
    street: str
    town: str
    postal_code: str


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


@router.get("/addresses/last/", tags=["addresses"])
async def get_last_address():
    """Get detail about an address"""

    addresses = Addresses().get_all_addresses()
    address = addresses[-1]
    return {"address": address}


@router.post("/addresses/", tags=["addresses"])
async def create_address(address: Address, hotel_id: int = 1):
    """Post detail about an address"""

    address = Addresses().create_address(address, hotel_id)
    return {"address": address}


@router.put("/addresses/{address_id}", tags=["addresses"])
async def update_address(address: Address, address_id: int = 1):
    """ Update address by its id. """

    if not Addresses().get_address_by_id(address_id):
        raise HTTPException(status_code=404, detail="Address not found")

    address = Addresses().update_address(address, address_id)
    return {"address": address}


@router.delete("/addresses/{address_id}", tags=["addresses"])
async def delete_address(address_id: int = 0):
    """ Delete address by its id. """

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
