"""Main app module to initialize the FastAPI framework."""
from users.routers import user
from fastapi import FastAPI

app = FastAPI()
app.include_router(user.router, tags=["users"])


@app.get("/")
def read_root():
    """Default root."""
    return {"message": "MyBookingServices"}
