"""Main app module to initialize the FastAPI framework."""
from management.routers import hotels
from management.routers import rooms
from management.routers import options
from fastapi import FastAPI

app = FastAPI()
app.include_router(hotels.router, tags=["hotels"])
app.include_router(rooms.router, tags=["rooms"])
app.include_router(options.router, tags=["options"])


@app.get("/")
def read_root():
    """Default root."""
    return {"message": "MyBookingServices"}
