from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_all_rooms():
    """List all rooms (default)"""
    expected = {
        "rooms": [
            {
                "id": 1,
                "hotel_id": 1,
                "room": "Suite",
                "price": 720.0,
                "capacity": 3,
            },
            {
                "id": 2,
                "hotel_id": 1,
                "room": "Junior suite",
                "price": 500.0,
                "capacity": 2,
            },
            {
                "id": 3,
                "hotel_id": 1,
                "room": "Chambre de luxe",
                "price": 300.0,
                "capacity": 2,
            },
            {
                "id": 4,
                "hotel_id": 1,
                "room": "Chambre standard",
                "price": 150.0,
                "capacity": 2,
            },
            {
                "id": 5,
                "hotel_id": 1,
                "room": "Chambre standard",
                "price": 150.0,
                "capacity": 2,
            },
            {
                "id": 6,
                "hotel_id": 2,
                "room": "Suite présidentielle",
                "price": 1000.0,
                "capacity": 5,
            },
            {
                "id": 7,
                "hotel_id": 2,
                "room": "Suite présidentielle",
                "price": 1000.0,
                "capacity": 5,
            },
        ],
    }
    response = client.get(
        "/rooms/all/",
    )
    assert response.status_code == 200
    assert response.json() == expected


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
        "/rooms/all/available/?hotel_id=1&start_date= \
        2021-07-21 & end_date=2021-07-23",
    )
    assert response.status_code == 200
    assert response.json() == expected


#
#
# def test_get_available_rooms_02():
#    """Test if dates are invalid."""
#    expected = {"detail":"Specified dates are invalid"}
#    response = client.get(
#        "/rooms/all/available/?hotel_id=1&start_date=2021-07-21&end_date=2021-07-23",
#    )
#    assert response.status_code == 400
#    assert response.json() == expected
#
#
# def test_get_available_rooms_03():
#    """Test available rooms with capacity."""
#    expected = {
#        "rooms": [
#            {
#                "id": 1,
#                "room": "Suite",
#                "price": 720,
#                "capacity": 3,
#            },
#        ],
#    }
#
#    response = client.get(
#        "/rooms/all/available/?hotel_id=1&start_date= \
#        2021-07-21&end_date=2021-07-23 \
#        &capacity=3",
#    )
#    assert response.status_code == 200
#    assert response.json() == expected
