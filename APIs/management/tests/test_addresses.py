from fastapi.testclient import TestClient
from management import app

client = TestClient(app.app)


def test_get_addresses_01():
    """ Test getting all addresses. """

    response = client.get("/addresses/all/")
    assert response.status_code == 200
    assert response.json() is not None


def test_get_last_address_01():
    """ Test getting the last address. """

    addresses = client.get("/addresses/all/").json()
    last_address = addresses["addresses"][-1]

    response = client.get("/addresses/last/")
    assert response.status_code == 200
    assert response.json()["address"] == last_address
    assert response.json() is not None


def test_get_one_addresses_01():
    """ Test getting address with id 1. """

    expect = {
        "address": {
            "id": 1,
            "hotel_id": 1,
            "number": "16",
            "street": "chemin Antoinette Duval",
            "town": "Gros",
            "postal_code": 23084,
        },
    }

    response = client.get("/addresses/1")
    assert response.status_code == 200
    assert response.json() == expect
    assert response.json() is not None


def test_get_unexisting_address_01():
    """ Test getting an unexisting address. """

    last_address = client.get("/addresses/last/").json()
    address_id = last_address["address"]["id"] + 1

    expect = {
        'detail': "Address not found",
    }

    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_create_address_01():
    """ Test creating address. """

    address = {
        "hotel_id": 2,
        "number": "42",
        "street": "rue de la vie",
        "town": "la terre",
        "postal_code": 77777,
    }

    response = client.post("/addresses/", json=address)
    last_address = client.get("/addresses/last/").json()

    assert response.status_code == 200
    assert response.json() == last_address
    assert response.json() is not None


def test_update_address_01():
    """ Test updating last inserted address. """

    address = {
        "hotel_id": 1,
        "number": "777",
        "street": "rue de la galaxy",
        "postal_code": 42042,
        "town": "Mars",
    }

    last_address = client.get("/addresses/last/").json()
    address_id = last_address["address"]["id"]

    response = client.put(f"/addresses/{address_id}", json=address)
    # TODO : Formattage bug
    # updated_address = client.get(f"/addresses/{address_id}")

    updated_address = {
        "address": {
            "id": address_id,
            "hotel_id": 1,
            "number": "777",
            "street": "rue de la galaxy",
            "postal_code": 42042,
            "town": "Mars",
        },
    }

    assert response.status_code == 200
    assert response.json() == updated_address
    assert response.json() is not None


def test_update_unexisting_address_01():
    """ Testing to update an unexisting address. """

    address = {
        "hotel_id": 2,
        "number": "123",
        "street": "rue de la la",
        "postal_code": 67890,
        "town": "null part",
    }

    expect = {
        'detail': "Address not found",
    }

    last_address = client.get("/addresses/last/").json()
    address_id = last_address["address"]["id"]
    address_id += 5

    response = client.put(f"/addresses/{address_id}", json=address)

    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_delete_address_01():
    """ Test deleting last inserted address. """

    address_id = client.get("/addresses/last/").json()["address"]["id"]

    response = client.delete(f"/addresses/{address_id}")
    deleted_address = client.get(f"/addresses/{address_id}")

    expect = {
        'detail': "Address not found",
    }

    assert response.status_code == 200
    assert response.json() == {}
    assert response.json() is not None
    assert deleted_address.status_code == 404
    assert deleted_address.json() == expect
    assert deleted_address.json() is not None
