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
                "number": "10",
                "street": "boulevard de Gros",
                "postal_code": 68649,
                "town": "Saint Joseph",
            },
            {
                "id": 2,
                "name": "Lutetia",
                "number": "246",
                "street": "chemin René Gaudin",
                "postal_code": 58613,
                "town": "Noelboeuf",
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
                "number": "246",
                "street": "chemin René Gaudin",
                "postal_code": 58613,
                "town": "Noelboeuf",
            },
        ],
    }

    response = client.get("/hotels/2")
    assert response.status_code == 200
    assert response.json() == expected
    assert response.json() is not None
