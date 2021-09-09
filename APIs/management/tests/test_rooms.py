from fastapi.testclient import TestClient
from management import app

client = TestClient(app.app)


def test_get_rooms_01():
    """ Test getting all rooms. """

    response = client.get("/rooms/all/")
    assert response.status_code == 200
    assert response.json() is not None


def test_get_last_room_01():
    """ Test getting the last room. """

    rooms = client.get("/rooms/all/").json()
    last_room = rooms["rooms"][-1]

    response = client.get("/rooms/last/")
    assert response.status_code == 200
    assert response.json()["room"] == last_room
    assert response.json() is not None


def test_get_one_rooms_01():
    """ Test getting room with id 1. """

    expect = {
        "room": {
            "id": 1,
            "hotel_id": 1,
            "room": "S",
            "price": 720.0,
            "capacity": 3,
        },
    }

    response = client.get("/rooms/1")
    assert response.status_code == 200
    assert response.json() == expect
    assert response.json() is not None


def test_get_unexisting_room_01():
    """ Test getting an unexisting room. """

    last_room = client.get("/rooms/last/").json()
    room_id = last_room["room"]["id"] + 1

    expect = {
        'detail': "Room not found",
    }

    response = client.get(f"/rooms/{room_id}")
    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_create_room_01():
    """ Test creating room. """

    room = {
        "hotel_id": 1,
        "room": "S",
        "price": 150,
        "capacity": 2,
    }

    response = client.post("/rooms", json=room)
    last_room = client.get("/rooms/last/").json()

    assert response.status_code == 200
    assert response.json() == last_room
    assert response.json() is not None


def test_update_room_01():
    """ Test updating last inserted room. """

    room = {
        "hotel_id": 1,
        "room": "S",
        "price": 150,
        "capacity": 2,
    }

    last_room = client.get("/rooms/last/").json()
    room_id = last_room["room"]["id"]

    response = client.put(f"/rooms/{room_id}", json=room)
    # TODO : Formattage bug
    # updated_room = client.get(f"/rooms/{room_id}")

    updated_room = {
        "room": {
            "id": room_id,
            "hotel_id": 1,
            "room": "S",
            "price": 150,
            "capacity": 2,
        },
    }

    assert response.status_code == 200
    assert response.json() == updated_room
    assert response.json() is not None


def test_update_unexisting_room_01():
    """ Testing to update an unexisting room. """

    room = {
        "hotel_id": 1,
        "room": "S",
        "price": 150,
        "capacity": 2,
    }

    expect = {
        'detail': "Room not found",
    }

    last_room = client.get("/rooms/last/").json()
    room_id = last_room["room"]["id"]
    room_id += 5

    response = client.put(f"/rooms/{room_id}", json=room)

    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_delete_room_01():
    """ Test deleting last inserted room. """

    room_id = client.get("/rooms/last/").json()["room"]["id"]

    response = client.delete(f"/rooms/{room_id}")
    deleted_room = client.get(f"/rooms/{room_id}")

    expect = {
        'detail': "Room not found",
    }

    assert response.status_code == 200
    assert response.json() == {}
    assert response.json() is not None
    assert deleted_room.status_code == 404
    assert deleted_room.json() == expect
    assert deleted_room.json() is not None
