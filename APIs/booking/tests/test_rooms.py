from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)
false = False


def test_get_room_info_by_id():
    response = client.get("/rooms/1")
    assert response.status_code == 200
    expected = {
        "room_id": [
            {
                "id": 1,
                "roomType": 1,
                "capacity": 2,
                "price": 5.4,
                "booked": false,
                "created_on": "2021-07-14T11:17:20",
                "updated_on": "2021-07-14T11:17:20",
            },
        ],
    }
    assert response.json() == expected
    assert response.json() is not None


def test_get_all_rooms():
    response = client.get("/rooms/all/")
    assert response.status_code == 200
    expected = {
        "rooms": [
            {
                "id": 1,
                "roomType": 1,
                "capacity": 2,
                "price": 5.4,
                "booked": false,
                "created_on": "2021-07-14T11:17:20",
                "updated_on": "2021-07-14T11:17:20",
            },
        ],
    }
    assert response.json() == expected
    assert response.json() is not None
