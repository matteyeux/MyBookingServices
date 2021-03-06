from fastapi.testclient import TestClient
from users import app

client = TestClient(app.app)
jwtoken = "TheToken"


def test_get_all_users_OK():
    """List all users (default)"""

    response = client.get(
        "/users/all/",
    )
    assert response.status_code == 200
    assert len(response.json()["users"]) == 500


def test_get_users_by_id_OK_user_1():
    expected = {
        "id": 1,
        "role": "ADMIN",
        "first_name": "Emmanuelle",
        "last_name": "Delaunay",
        "email": "admin0@mybooking.services",
        "telephone": "0424716847",
    }

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_users_by_id_OK_user_24():
    expected = {
        "id": 24,
        "role": "USER",
        "first_name": "Corinne",
        "last_name": "Dumont",
        "email": "umahe@ifrance.com",
        "telephone": "+33 (0)3 58 17 46 50",
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


def test_login_OK():
    response = client.post(
        "/users/login",
        json={
            "email": "admin0@mybooking.services",
            "password": "XM9TxmUH*1MY",
        },
    )

    assert response.status_code == 200
    assert response.json() is not None
    global jwtoken
    jwtoken = response.json()["access_token"]
    assert jwtoken != "TheToken"


def test_get_user_me_OK():
    expected = {
        "id": 1,
        "role": "ADMIN",
        "first_name": "Emmanuelle",
        "last_name": "Delaunay",
        "email": "admin0@mybooking.services",
        "telephone": "0424716847",
    }

    headers = {
        "Authorization": "Bearer " + jwtoken,
    }

    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == expected


def test_get_me_KO_not_logged():
    response = client.get("/users/me")
    assert response.status_code == 403
