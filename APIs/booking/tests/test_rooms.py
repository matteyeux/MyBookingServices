from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_available_rooms_01():
    """Test available rooms without capacity."""
    expected = {
        "rooms": [
            {
                "id": 1,
                "room": "Suite",
                "price": 720,
                "capacity": 3,
            },
            {
                "id": 3,
                "room": "Chambre de luxe",
                "price": 300,
                "capacity": 2,
            },
            {
                "id": 4,
                "room": "Chambre standard",
                "price": 150,
                "capacity": 2,
            },
            {
                "id": 5,
                "room": "Chambre standard",
                "price": 150,
                "capacity": 2,
            },
        ],
    }
    response = client.get(
        "/rooms/all/available/?hotel_id=1&start_date=2021-07-21&end_date=2021-07-23",
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_available_rooms_02():
    """Test available rooms with capacity."""
    expected = {
        "rooms": [
            {
                "id": 1,
                "room": "Suite",
                "price": 720,
                "capacity": 3,
            },
        ],
    }

    response = client.get(
        "/rooms/all/available/?hotel_id=1&start_date=2021-07-21&end_date=2021-07-23 \
        &capacity=3",
    )
    assert response.status_code == 200
    assert response.json() == expected
