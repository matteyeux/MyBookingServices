from fastapi.testclient import TestClient
from management import app

client = TestClient(app.app)


def test_get_price_policies_01():
    """ Test getting all price_policies. """

    response = client.get("/price_policies/all/")
    assert response.status_code == 200
    assert response.json() is not None


def test_get_last_price_policy_01():
    """ Test getting the last price_policy. """

    price_policies = client.get("/price_policies/all/").json()
    last_price_policy = price_policies["price_policies"][-1]

    response = client.get("/price_policies/last/")
    assert response.status_code == 200
    assert response.json()["price_policy"] == last_price_policy
    assert response.json() is not None


def test_get_one_price_policies_01():
    """ Test getting price_policy with id 1. """

    expect = {
        "price_policy": [
            {
                "id": 1,
                "room_id": 1,
                "name": "Wednesday Minoration",
                "room_majoration": -10.0,
                "price_policy_type": 1,
                "day_number": 3,
                "capacity_limit": None,
                "is_default": True,
                "majoration_start_date": None,
                "majoration_end_date": None,
            },
        ],
    }

    response = client.get("/price_policies/1")
    assert response.status_code == 200
    assert response.json() == expect
    assert response.json() is not None


def test_get_unexisting_price_policy_01():
    """ Test getting an unexisting price_policy. """

    last_price_policy = client.get("/price_policies/last/").json()
    price_policy_id = last_price_policy["price_policy"]["id"] + 1

    expect = {
        'detail': "price_policy not found",
    }

    response = client.get(f"/price_policies/{price_policy_id}")
    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_create_price_policy_01():
    """ Test creating price_policy. """

    price_policy = {
        "name": "Un ajout",
        "room_id": 1,
        "room_majoration": -50.0,
        "price_policy_type": 2,
        "day_number": 3,
        "capacity_limit": 2,
        "is_default": True,
        "majoration_start_date": None,
        "majoration_end_date": None,
    }

    response = client.post("/price_policies", json=price_policy)
    last_price_policy = client.get("/price_policies/last/").json()

    assert response.status_code == 200
    assert response.json() == last_price_policy
    assert response.json() is not None


def test_update_price_policy_01():
    """ Test updating last inserted price_policy. """

    price_policy = {
        "name": "Une réussite",
        "room_id": 2,
        "room_majoration": -500.0,
        "price_policy_type": 1,
        "day_number": 5,
        "capacity_limit": 10,
        "is_default": True,
        "majoration_start_date": None,
        "majoration_end_date": None,
    }

    last_price_policy = client.get("/price_policies/last/").json()
    price_policy_id = last_price_policy["price_policy"]["id"]

    response = client.put(
        f"/price_policies/{price_policy_id}",
        json=price_policy,
    )
    # TODO : Formattage bug
    # updated_price_policy = client.get(f"/price_policies/{price_policy_id}")

    updated_price_policy = {
        "price_policy": {
            "id": price_policy_id,
            "name": "Une réussite",
            "room_id": 2,
            "room_majoration": -500.0,
            "price_policy_type": 1,
            "day_number": 5,
            "capacity_limit": 10,
            "is_default": True,
            "majoration_start_date": None,
            "majoration_end_date": None,
        },
    }

    assert response.status_code == 200
    assert response.json() == updated_price_policy
    assert response.json() is not None


def test_update_unexisting_price_policy_01():
    """ Testing to update an unexisting price_policy. """

    price_policy = {
        "name": "Un échec",
        "room_id": 4,
        "room_majoration": -999999.9,
        "price_policy_type": 1,
        "day_number": 1,
        "capacity_limit": 100,
        "is_default": True,
        "majoration_start_date": None,
        "majoration_end_date": None,
    }

    expect = {
        'detail': "price_policy not found",
    }

    last_price_policy = client.get("/price_policies/last/").json()
    price_policy_id = last_price_policy["price_policy"]["id"]
    price_policy_id += 5

    response = client.put(
        f"/price_policies/{price_policy_id}",
        json=price_policy,
    )

    assert response.status_code == 404
    assert response.json() == expect
    assert response.json() is not None


def test_delete_price_policy_01():
    """ Test deleting last inserted price_policy. """

    price_policy_id = client.get("/price_policies/last/").json()[
        "price_policy"
    ]["id"]

    response = client.delete(f"/price_policies/{price_policy_id}")
    deleted_price_policy = client.get(f"/price_policies/{price_policy_id}")

    expect = {
        'detail': "price_policy not found",
    }

    assert response.status_code == 200
    assert response.json() == {}
    assert response.json() is not None
    assert deleted_price_policy.status_code == 404
    assert deleted_price_policy.json() == expect
    assert deleted_price_policy.json() is not None
