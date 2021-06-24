from booking.app import app


@app.get("/book")
def book():
    """Book room"""
    return {"test": "test"}
