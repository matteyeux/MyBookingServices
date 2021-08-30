from fastapi.testclient import TestClient
from users import app

client = TestClient(app.app)


def test_get_all_users_OK():
    """List all users (default)"""

    response = client.get(
        "/users/all/",
    )
    assert response.status_code == 200
    assert len(response.json()["users"]) == 500


def test_get_users_by_id_OK_user_1():
    expected = {
        "user": [
            {
                "id": 1,
                "first_name": "Zacharie",
                "last_name": "Toussaint",
                "email": "jpoirier@free.fr",
                "telephone": "+33 4 23 08 57 92",
                "username": "jason47",
                "password": "i085xZGalL$3",
                "created_time": "2021-08-17T20:48:10",
                "updated_time": "2021-08-17T20:48:10",
            },
        ],
    }

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_users_by_id_OK_user_24():
    expected = {
        "user": [
            {
                "id": 24,
                "first_name": "Claire",
                "last_name": "Begue",
                "email": "lucasriviere@laposte.net",
                "telephone": "0330109236",
                "username": "josecastillo",
                "password": "5lUJcSvr5(9h",
                "created_time": "2021-08-17T20:48:10",
                "updated_time": "2021-08-17T20:48:10",
            },
        ],
    }

    response = client.get("/users/24")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_users_by_id_KO_bad_request():
    expected = {
        "detail": "Can't use id <= 0",
    }

    response = client.get("/users/-1")
    assert response.status_code == 400
    assert response.json() == expected


def test_get_users_by_id_KO_not_found():
    expected = {
        "detail": "User not found",
    }

    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json() == expected
