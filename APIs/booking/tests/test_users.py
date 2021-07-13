from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    expected = [{"username": "Rick"}, {"username": "Morty"}]
    assert response.json() == expected
    assert response.json() is not None


def test_read_user_me():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"username": "fakecurrentuser"}
    assert response.json() is not None


def test_read_user():
    response = client.get("/users/hello")
    assert response.status_code == 200
    assert response.json() == {"username": "hello"}
    assert response.json() is not None
