from fastapi.testclient import TestClient
from management import app

client = TestClient(app.app)


def test_get_options_01():
    """ Test getting all options. """

    response = client.get("/options/all/")
    assert response.status_code == 200
    assert response.json() is not None


def test_get_last_option_01():
    """ Test getting the last option. """

    options = client.get("/options/all/").json()
    last_option = options["options"][-1]

    response = client.get("/options/last/")
    assert response.status_code == 200
    assert response.json()["option"] == last_option
    assert response.json() is not None


def test_get_one_options_01():
    """ Test getting option with id 1. """

    expect = {
        "option": [
            {
                "id": 1,
                "name": "Parking",
                "price": 25,
            },
        ],
    }

    response = client.get("/options/1")
    assert response.status_code == 200
    assert response.json() == expect
    assert response.json() is not None


def test_get_unexisting_option_01():
    """ Test getting an unexisting option. """

    last_option = client.get("/options/last/").json()
    option_id = last_option["option"]["id"] + 1

    expect = {
        'detail': "Option not found",
    }

    response = client.get(f"/options/{option_id}")
    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_create_option_01():
    """ Test creating option. """

    option = {
        "name": "tested",
        "price": 50,
    }

    response = client.post("/options", json=option)
    last_option = client.get("/options/last/").json()

    assert response.status_code == 200
    assert response.json() == last_option
    assert response.json() is not None


def test_update_option_01():
    """ Test updating last inserted option. """

    option = {
        "name": "updated",
        "price": 51234,
    }

    last_option = client.get("/options/last/").json()
    option_id = last_option["option"]["id"]

    response = client.put(f"/options/{option_id}", json=option)
    # TODO : Formattage bug
    # updated_option = client.get(f"/options/{option_id}")

    updated_option = {
        "option": {
            "id": option_id,
            "name": "updated",
            "price": 51234,
        },
    }

    assert response.status_code == 200
    assert response.json() == updated_option
    assert response.json() is not None


def test_update_unexisting_option_01():
    """ Testing to update an unexisting option. """

    option = {
        "name": "updated",
        "price": 51234,
    }

    expect = {
        'detail': "Option not found",
    }

    last_option = client.get("/options/last/").json()
    option_id = last_option["option"]["id"]
    option_id += 5

    response = client.put(f"/options/{option_id}", json=option)

    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_delete_option_01():
    """ Test deleting last inserted option. """

    option_id = client.get("/options/last/").json()["option"]["id"]

    response = client.delete(f"/options/{option_id}")
    deleted_option = client.get(f"/options/{option_id}")

    expect = {
        'detail': "Option not found",
    }

    assert response.status_code == 200
    assert response.json() == {}
    assert response.json() is not None
    assert deleted_option.status_code == 404
    assert deleted_option.json() == expect
    assert deleted_option.json() is not None
