from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_get_hotels_01():
    """Test get all hotels."""
    expected = {
        "hotels": [
            {
                "id": 1,
                "name": "Carlton",
                "number": "85",
                "street": "avenue Nicole Blanchet",
                "postal_code": 19067,
                "town": "Paris-sur-Reynaud",
            },
            {
                "id": 2,
                "name": "Lutetia",
                "number": "857",
                "street": "chemin Thierry Langlois",
                "postal_code": 45467,
                "town": "Saint MargotVille",
            },
        ],
    }
    response = client.get("/hotels/all/")
    assert response.status_code == 200
    assert response.json() == expected
    assert response.json() is not None


def test_get_hotel_by_id_01():
    """Test get hotel by ID."""
    expected = {
        "hotel": [
            {
                "id": 2,
                "name": "Lutetia",
                "number": "857",
                "street": "chemin Thierry Langlois",
                "postal_code": 45467,
                "town": "Saint MargotVille",
            },
        ],
    }
    response = client.get("/hotels/2")
    assert response.status_code == 200
    assert response.json() == expected
    assert response.json() is not None
