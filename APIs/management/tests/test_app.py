from management import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MyBookingServices"}
    assert response.json() is not None
