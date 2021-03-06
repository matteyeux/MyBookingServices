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
                "number": "16",
                "street": "chemin Antoinette Duval",
                "postal_code": 23084,
                "town": "Gros",
            },
            {
                "id": 2,
                "name": "Lutetia",
                "number": "39",
                "street": "boulevard Leclerc",
                "postal_code": 91285,
                "town": "Sainte Matthieuboeuf",
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
                "number": "39",
                "street": "boulevard Leclerc",
                "postal_code": 91285,
                "town": "Sainte Matthieuboeuf",
            },
        ],
    }

    response = client.get("/hotels/2")
    assert response.status_code == 200
    assert response.json() == expected
    assert response.json() is not None
