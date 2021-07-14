from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_room_info_by_id():
    response = client.get("/rooms/1")
    assert response.status_code == 200
    assert response.json()['room_id'][0]['id'] == 1
    assert response.json() is not None


def test_get_all_rooms():
    response = client.get("/rooms/all/")
    assert response.status_code == 200
    assert response.json()['rooms'][0]['id'] == 1
    assert response.json() is not None
