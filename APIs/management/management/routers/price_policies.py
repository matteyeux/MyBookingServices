from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from management.models.price_policies import Price_Policies
from management.utils import user_is_admin
from management.utils import user_logged
from pydantic import BaseModel

# from sqlalchemy.sql.sqltypes import Integer

router = APIRouter()


class Price_Policy(BaseModel):
    name: str
    room_id: int
    price_policy_type: int
    room_majoration: float
    day_number: int
    capacity_limit: int
    majoration_start_date: Optional[datetime] = None
    majoration_end_date: Optional[datetime] = None
    is_default: bool


@router.get("/price_policies/all/", tags=["price_policies"])
async def get_all_price_policies():
    """Get all price_policies."""

    price_policies = Price_Policies().get_all_price_policies()
    return {"price_policies": price_policies}


@router.get("/price_policies/last/", tags=["price_policies"])
async def get_last_price_policy():
    """Get last inserted price_policy."""

    price_policies = Price_Policies().get_all_price_policies()
    last_price_policy = price_policies[-1]
    return {"price_policy": last_price_policy}


@router.post("/price_policies", tags=["price_policies"])
async def add_new_price_policy(request: Request, price_policy: Price_Policy):
    """Add a new price_policy."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    price_policy = Price_Policies().add_price_policy(price_policy)
    return {"price_policy": price_policy}


@router.get("/price_policies/{price_policy_id}", tags=["price_policies"])
async def get_price_policy_by_id(price_policy_id: int = 1):
    """Get one price_policy by its id."""

    price_policy = Price_Policies().get_price_policy_by_id(price_policy_id)
    if not price_policy:
        raise HTTPException(status_code=404, detail="price_policy not found")
    return {"price_policy": price_policy}


@router.put("/price_policies/{price_policy_id}", tags=["price_policies"])
async def update_price_policy(
    request: Request,
    price_policy: Price_Policy,
    price_policy_id: int = 1,
):
    """Update price_policy by its id."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    if not Price_Policies().get_price_policy_by_id(price_policy_id):
        raise HTTPException(status_code=404, detail="price_policy not found")

    price_policy = Price_Policies().update_price_policy(
        price_policy,
        price_policy_id,
    )
    return {"price_policy": price_policy}


@router.delete("/price_policies/{price_policy_id}", tags=["price_policies"])
async def delete_price_policy(request: Request, price_policy_id: int = 0):
    """Delete price_policy by its id."""

    user = user_logged(request.headers.get("authorization"))
    user_is_admin(user)

    if price_policy_id > 0:
        price_policy = Price_Policies().delete_price_policy(price_policy_id)

        if not price_policy:
            raise HTTPException(
                status_code=404,
                detail="price_policy not found",
            )

        return price_policy
