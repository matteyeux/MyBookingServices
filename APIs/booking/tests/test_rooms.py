from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_room_info_by_id_01():
    """Check happy path."""
    response = client.get("/rooms/1")
    assert response.status_code == 200
    assert response.json()['room_id'][0]['id'] == 1
    assert response.json() is not None


def test_get_room_info_by_id_02():
    """Check 404 on room ID."""
    response = client.get("/rooms/12345")
    assert response.status_code == 404
    assert response.json()['detail'] == "Room not found"


def test_get_room_info_by_id_03():
    """Check 400 on room ID = 0."""
    response = client.get("/rooms/0")
    assert response.status_code == 400
    assert response.json()['detail'] == "Can't use id <= 0"


def test_get_all_rooms_01():
    response = client.get("/rooms/all/")
    assert response.status_code == 200
    assert response.json()['rooms'][0]['id'] == 1
    assert response.json() is not None
