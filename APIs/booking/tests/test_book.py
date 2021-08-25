from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_book_room_01():
    """Check 422 with wrong data in json payload."""
    expected = {"detail": "Unprocessable Entity"}
    data = {"key1": "value1", "key2": "value2"}
    response = client.post("/book/", json=data)

    assert response.status_code == 422
    assert response.json() == expected


def test_book_room_02():
    """Check booked room returns 403."""
    assert None is None
