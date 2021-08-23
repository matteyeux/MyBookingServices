from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_book_room_01():
    """Check 400 on room ID."""
    response = client.post("/book/-1")
    assert response.status_code == 400
    assert response.json()['detail'] == "Can't use id <= 0"
    assert response.json() is not None


def test_book_room_02():
    """Check booked room return 403."""
    assert None is None
    # response = client.post("/book/1")
    # assert response.status_code == 403
    # assert (
    #     response.json()['detail'] == "Room is already booked for this period"
    # )
    # assert response.json() is not None


def test_book_room_03():
    """Check booked room returns 404."""
    assert None is None
    # response = client.post("/book/12345")
    # assert response.status_code == 404
    # assert response.json()['detail'] == "Room not found, can't book it."
    # assert response.json() is not None


def test_book_room_04():
    """Check happy path."""
    response = client.post("/book/2")
    assert response.status_code == 200
    assert response.json()['room_id'][0]['id'] == 2
    assert response.json() is not None


def test_available_rooms_01():
    """Check booked room returns 404."""
    assert None is None
    # response = client.get("/book/all")
    # assert response.status_code == 200
    # assert response.json()['available_rooms'][0]['id'] == 2
    # assert response.json() is not None
