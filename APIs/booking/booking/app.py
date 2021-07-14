"""Main app module to initialize the FastAPI framework."""
from booking.routers import book
from booking.routers import rooms
from fastapi import FastAPI

app = FastAPI()
app.include_router(rooms.router, tags=["rooms"])
app.include_router(book.router, tags=["book"])


@app.get("/")
def read_root():
    """Default root."""
    return {"message": "Welcome to MyBookingServices"}
