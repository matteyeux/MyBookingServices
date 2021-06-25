"""Main app module to initialize the FastAPI framework."""
# from typing import Optional
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    """Default root."""
    return {"message": "Hello World"}


def run_server():
    """Init API server."""
    uvicorn.run("booking.app:app", host="127.0.0.1", port=5000, reload=True)
