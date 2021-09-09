"""Main app module to initialize the FastAPI framework."""
from fastapi import FastAPI
from management.routers import addresses
from management.routers import hotels
from management.routers import options
from management.routers import price_policies
from management.routers import rooms

app = FastAPI()
app.include_router(hotels.router, tags=["hotels"])
app.include_router(rooms.router, tags=["rooms"])
app.include_router(options.router, tags=["options"])
app.include_router(price_policies.router, tags=["price_policy"])
app.include_router(addresses.router, tags=["addresses"])


@app.get("/")
def read_root():
    """Default root."""
    return {"message": "MyBookingServices"}
