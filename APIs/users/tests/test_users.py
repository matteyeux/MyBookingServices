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
        "id": 1,
        "role": "USER",
        "first_name": "Isabelle",
        "last_name": "Gomes",
        "email": "allainmargot@dbmail.com",
        "telephone": "0123254441",
    }

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_users_by_id_OK_user_24():
    expected = {
        "id": 24,
        "role": "USER",
        "first_name": "Aurélie",
        "last_name": "Boucher",
        "email": "laportepierre@voila.fr",
        "telephone": "+33 3 23 28 66 20",
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
