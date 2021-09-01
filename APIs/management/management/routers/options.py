from management.models.options import Options
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

# from fastapi import Request

router = APIRouter()


class Option(BaseModel):
    name: str
    price: float

@router.get("/options/all/", tags=["options"])
async def get_options():
    """ Get all options."""
    options = Options().get_all_options()

    return {"options": options}

@router.get("/options/{option_id}", tags=["options"])
async def get_option_by_id(option_id: int = 1):
    """ Get one option by its id. """
    option = Options().get_option_by_id(option_id)
    return {"option": option}

@router.post("/options", tags=["options"])
async def add_new_option(option: Option):
    """ Add a new option"""
    option = Options().add_option(option)
    return {"option": option}

@router.put("/options/{option_id}", tags=["options"])
async def update_option(option: Option, option_id: int = 1):
    """ Update option's price """
    option = Options().update_option(option, option_id)
    return {"option": option}

@router.delete("/options/{option_id}", tags=["options"])
async def delete_option(option_id: int = 0):
    if option_id > 0:
        option = Options().delete_option(option_id)
        return "ok"
