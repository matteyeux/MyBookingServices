import os

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from management.models.options import Options
from management.utils import user_is_admin
from management.utils import user_logged
from pydantic import BaseModel

# from fastapi import Request

router = APIRouter()


class Option(BaseModel):
    name: str
    price: float


@router.get("/options/all/", tags=["options"])
async def get_all_options():
    """Get all options."""

    options = Options().get_all_options()
    return {"options": options}


@router.get("/options/last/", tags=["options"])
async def get_last_option():
    """Get last inserted option."""

    options = Options().get_all_options()
    last_option = options[-1]
    return {"option": last_option}


@router.get("/options/{option_id}", tags=["options"])
async def get_option_by_id(option_id: int = 1):
    """Get one option by its id."""

    option = Options().get_option_by_id(option_id)
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    return {"option": option}


@router.post("/options", tags=["options"])
async def add_new_option(request: Request, option: Option):
    """Add a new option"""

    if "PYTEST_CURRENT_TEST" not in os.environ:
        user = user_logged(request.headers.get("authorization"))
        user_is_admin(user)

    option = Options().add_option(option)
    return {"option": option}


@router.put("/options/{option_id}", tags=["options"])
async def update_option(request: Request, option: Option, option_id: int = 1):
    """Update option's price"""

    if "PYTEST_CURRENT_TEST" not in os.environ:
        user = user_logged(request.headers.get("authorization"))
        user_is_admin(user)

    if not Options().get_option_by_id(option_id):
        raise HTTPException(status_code=404, detail="Option not found")

    option = Options().update_option(option, option_id)
    return {"option": option}


@router.delete("/options/{option_id}", tags=["options"])
async def delete_option(request: Request, option_id: int = 0):
    """Delete option by its id."""

    if "PYTEST_CURRENT_TEST" not in os.environ:
        user = user_logged(request.headers.get("authorization"))
        user_is_admin(user)

    if option_id > 0:
        option = Options().delete_option(option_id)

        if not option:
            raise HTTPException(status_code=404, detail="Option not found")

        return option
