"""Main app module to initialize the FastAPI framework."""
# from typing import Optional
from booking.routers import users
from fastapi import APIRouter


app = APIRouter()
app.include_router(users.router, tags=["users"])


@app.get("/")
def read_root():
    """Default root."""
    return {"message": "Hello World"}
