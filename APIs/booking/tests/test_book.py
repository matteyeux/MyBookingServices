from booking import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_book_room_01():
    """Check 422 with wrong data in json payload."""
    expected = {"detail": "Unprocessable Entity"}
    data = {"key1": "value1", "key2": "value2"}
    response = client.post("/book/", json=data)

    assert response.status_code == 422
    assert response.json() == expected


def test_book_room_02():
    """Check booked room returns 403."""
    data = {
        'hotel_id': 1,
        'room_id': 3,
        'start_date': '2021-10-27',
        'end_date': '2021-10-30',
        'capacity': 2,
        'options': {
            'parking': 1,
            'baby_cot': 1,
            'romance_pack': 1,
            'breakfast': 1,
        },
    }
    expected = {"detail": "Room is already booked for this period"}

    response = client.post("/book/", json=data)

    assert response.status_code == 403
    assert response.json() == expected


# def test_book_room_03():
#   """Book room. Exected content is meant to change when pricing is done."""
#   data = {
#       'hotel_id': 1,
#       'room_id': 1,
#       'start_date': '2021-10-27',
#       'end_date': '2021-10-30',
#       'capacity': 2,
#       'options': {
#           'parking': 1,
#           'baby_cot': 1,
#           'romance_pack': 1,
#           'breakfast': 1,
#       },
#   }
#
#   expected = {
#       "room": {
#           "hotel_id": 1,
#           "room_id": 1,
#           "start_date": "2021-10-27",
#           "end_date": "2021-10-30",
#           "capacity": 2,
#           "options": {
#               "parking": 1,
#               "baby_cot": 1,
#               "romance_pack": 1,
#               "breakfast": 1,
#           },
#       },
#   }
#   response = client.post("/book/", json=data)
#
#   assert response.status_code == 200
#   assert response.json() == expected
