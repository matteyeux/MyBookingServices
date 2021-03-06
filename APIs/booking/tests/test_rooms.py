from shutil import copyfile

from booking import app
from booking import config
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_all_rooms_01():
    """List all rooms (default)"""
    expected = {
        "rooms": [
            {
                "id": 1,
                "hotel_id": 1,
                "room": "S",
                "price": 720,
                "capacity": 3,
            },
            {
                "id": 2,
                "hotel_id": 1,
                "room": "JS",
                "price": 500,
                "capacity": 2,
            },
            {
                "id": 3,
                "hotel_id": 1,
                "room": "CD",
                "price": 300,
                "capacity": 2,
            },
            {
                "id": 4,
                "hotel_id": 1,
                "room": "CS",
                "price": 150,
                "capacity": 2,
            },
            {
                "id": 5,
                "hotel_id": 1,
                "room": "CS",
                "price": 150,
                "capacity": 2,
            },
            {
                "id": 6,
                "hotel_id": 2,
                "room": "SR",
                "price": 1000,
                "capacity": 5,
            },
            {
                "id": 7,
                "hotel_id": 2,
                "room": "SR",
                "price": 1000,
                "capacity": 5,
            },
        ],
    }

    response = client.get(
        "/rooms/all/",
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_all_rooms_02():
    """List all rooms for an hotel_id"""
    expected = {
        "rooms": [
            {
                "id": 6,
                "hotel_id": 2,
                "room": "SR",
                "price": 1000,
                "capacity": 5,
            },
            {
                "id": 7,
                "hotel_id": 2,
                "room": "SR",
                "price": 1000,
                "capacity": 5,
            },
        ],
    }

    response = client.get(
        "/rooms/all/?&hotel_id=2",
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_all_rooms_03():
    """List all rooms for hotel_id=2 and capacity = 7
    Json should me empty.
    """
    expected = {
        "rooms": [],
    }

    response = client.get(
        "/rooms/all/?&hotel_id=2&capacity=7",
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_available_rooms_01():
    """Test available rooms without capacity."""
    expected = {
        "rooms": [
            {
                "id": 2,
                "hotel_id": 1,
                "room": "JS",
                "price": 500,
                "capacity": 2,
            },
            {
                "id": 3,
                "hotel_id": 1,
                "room": "CD",
                "price": 300,
                "capacity": 2,
            },
            {
                "id": 5,
                "hotel_id": 1,
                "room": "CS",
                "price": 150,
                "capacity": 2,
            },
        ],
    }
    response = client.get(
        "/rooms/all/available/?hotel_id=1 \
        &start_date=2021-09-18&end_date=2021-09-30",
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_available_rooms_02():
    """Test available rooms without capacity."""
    expected = {
        "detail": "Specified dates are invalid",
    }

    response = client.get(
        "/rooms/all/available/?hotel_id=1&end_date=2021-09-30",
    )
    assert response.status_code == 400
    assert response.json() == expected


def test_get_available_rooms_03():
    """Test available rooms without bad mysql database."""
    expected = {
        "detail": "Service Unavailable",
    }

    # get config file
    _, config_file = config.get_config()

    content = open(config_file).read()
    copyfile(config_file, f"{config_file}.bak")

    # replace content with wrong data
    # and write to new config file
    open(config_file, 'w').write(content.replace("etna", "baduser"))

    response = client.get(
        "/rooms/all/available/?hotel_id=1 \
        &start_date=2021-09-18&end_date=2021-09-30",
    )
    assert response.status_code == 500
    assert response.json() == expected

    # rollback
    copyfile(f"{config_file}.bak", config_file)


def test_get_rooms_by_id_01():
    expected = {
        "room_id": [
            {
                "id": 1,
                "hotel_id": 1,
                "room": "S",
                "capacity": 3,
                "price": 720,
                "created_time": "2021-09-05T11:24:31",
                "updated_time": "2021-09-05T11:24:31",
            },
        ],
    }

    response = client.get("/rooms/1")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_rooms_by_id_02():
    expected = {
        "detail": "Can't use id <= 0",
    }

    response = client.get("/rooms/-1")
    assert response.status_code == 400
    assert response.json() == expected


def test_get_rooms_by_id_03():
    expected = {
        "detail": "Room not found",
    }

    response = client.get("/rooms/404")
    assert response.status_code == 404
    assert response.json() == expected


def test_get_all_options():
    """List all options for rooms."""
    expected = {
        "options": [
            {"id": 1, "name": "Parking", "price": 25.0},
            {"id": 2, "name": "Baby cot", "price": 0.0},
            {
                "id": 3,
                "name": "Romance pack",
                "price": 50.0,
            },
            {"id": 4, "name": "Breakfast", "price": 30.0},
        ],
    }

    response = client.get(
        "/rooms/options/",
    )
    assert response.status_code == 200
    assert response.json() == expected
