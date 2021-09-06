from fastapi.testclient import TestClient
from management import app

client = TestClient(app.app)


def test_get_hotels_01():
    """ Test getting all hotels. """

    response = client.get("/hotels/all/")
    assert response.status_code == 200
    assert response.json() is not None


def test_get_last_hotel_01():
    """ Test getting the last hotel. """

    hotels = client.get("/hotels/all/").json()
    last_hotel = hotels["hotels"][-1]

    response = client.get("/hotels/last/")
    assert response.status_code == 200
    assert response.json()["hotel"] == last_hotel
    assert response.json() is not None


def test_get_one_hotels_01():
    """ Test getting hotel with id 1. """

    expect = {
        "hotel": {
            "id": 1,
            "name": "Carlton",
            "telephone": "02 55 03 05 09",
            "website": "https://www.de.com/privacy.asp",
            "description": "Le pouvoir d'évoluer naturellement",
            "owner": "Geneviève Rolland-Carre",
            "number": "16",
            "street": "chemin Antoinette Duval",
            "postal_code": 23084,
            "town": "Gros",
        },
    }

    response = client.get("/hotels/1")
    assert response.status_code == 200
    assert response.json() == expect
    assert response.json() is not None


def test_get_unexisting_hotel_01():
    """ Test getting an unexisting hotel. """

    last_hotel = client.get("/hotels/last/").json()
    hotel_id = last_hotel["hotel"]["id"] + 1

    expect = {
        'detail': "Hotel not found",
    }

    response = client.get(f"/hotels/{hotel_id}")
    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_create_hotel_01():
    """ Test creating hotel. """

    hotel = {
        "hotel": {
            "name": "Blue Palace",
            "telephone": "0899112233",
            "website": "http://www.matteyeux.com",
            "description": "Une description",
            "owner": "Un Péon",
        },
        "address": {
            "number": "42",
            "street": "cred zer",
            "postal_code": 75001,
            "town": "Montcucq",
        },
    }

    response = client.post("/hotels/", json=hotel)
    last_hotel = client.get("/hotels/last/").json()

    assert response.status_code == 200
    assert response.json() == last_hotel
    assert response.json() is not None


def test_update_hotel_01():
    """ Test updating last inserted hotel. """

    hotel = {
        "name": "Green Lantern",
        "telephone": "0123456789",
        "website": "http://www.le-vide-intersideral.com",
        "description": "je ne sais pas",
        "owner": "bâton sacré",
    }

    last_hotel = client.get("/hotels/last/").json()
    hotel_id = last_hotel["hotel"]["id"]

    response = client.put(f"/hotels/{hotel_id}", json=hotel)
    # TODO : Formattage bug
    # updated_hotel = client.get(f"/hotels/{hotel_id}")

    updated_hotel = {
        "hotel": {
            "id": hotel_id,
            "name": "Green Lantern",
            "telephone": "0123456789",
            "website": "http://www.le-vide-intersideral.com",
            "description": "je ne sais pas",
            "owner": "bâton sacré",
        },
    }

    assert response.status_code == 200
    assert response.json() == updated_hotel
    assert response.json() is not None


def test_update_unexisting_hotel_01():
    """ Testing to update an unexisting hotel. """

    hotel = {
        "name": "Green Lantern",
        "telephone": "0123456789",
        "website": "http://www.le-vide-intersideral.com",
        "description": "je ne sais pas",
        "owner": "bâton sacré",
    }

    expect = {
        'detail': "Hotel not found",
    }

    last_hotel = client.get("/hotels/last/").json()
    hotel_id = last_hotel["hotel"]["id"]
    hotel_id += 5

    response = client.put(f"/hotels/{hotel_id}", json=hotel)

    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_delete_hotel_01():
    """ Test deleting last inserted hotel. """

    hotel_id = client.get("/hotels/last/").json()["hotel"]["id"]

    response = client.delete(f"/hotels/{hotel_id}")
    # deleted_hotel = client.get(f"/hotels/{hotel_id}")

    # expect = {
    #     'detail': "hotel not found",
    # }

    assert response.status_code == 400
    assert response.json() == {"detail": "Cascade deletion impossible"}
    assert response.json() is not None
    # assert deleted_hotel.status_code == 404
    # assert deleted_hotel.json() == expect
    # assert deleted_hotel.json() is not None
