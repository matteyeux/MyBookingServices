from booking import utils


def test_check_dates_01():
    """check dates"""
    start = "2021-09-09"
    end = "2021-09-09"
    assert utils.check_dates(start, end) is False


def test_handle_pricing_01():
    """basic pricing."""
    assert None is None


def test_book_sanity_check_01():
    """check if all keys are there."""
    valid_json = {
        "room_id": 1,
        "start_date": "2021-10-08",
        "end_date": "2021-10-11",
        "capacity": 2,
        "options": {
            "parking": 1,
            "baby_cot": 1,
            "romance_pack": 1,
            "breakfast": 1,
        },
    }
    assert utils.book_sanity_check(valid_json) is True


def test_book_sanity_check_02():
    """remove one key should make in invalid."""
    invalid_json = {
        "start_date": "2021-10-08",
        "end_date": "2021-10-11",
        "capacity": 2,
        "options": {
            "parking": 1,
            "baby_cot": 1,
            "romance_pack": 1,
            "breakfast": 1,
        },
    }
    assert utils.book_sanity_check(invalid_json) is False


def test_book_sanity_check_03():
    """check dates, start date is set to 2020."""
    json_bad_dates = {
        "room_id": 1,
        "start_date": "2020-10-08",
        "end_date": "2021-10-11",
        "capacity": 2,
    }
    assert utils.book_sanity_check(json_bad_dates) is False


def test_book_sanity_check_04():
    """check room_id is not neg."""
    room_neg_json = {
        "room_id": -1,
        "start_date": "2021-10-08",
        "end_date": "2021-10-11",
        "capacity": 2,
        "options": {
            "parking": 1,
            "baby_cot": 1,
            "romance_pack": 1,
            "breakfast": 1,
        },
    }
    assert utils.book_sanity_check(room_neg_json) is False


def test_book_sanity_check_05():
    """check if room exists."""
    no_room_json = {
        "room_id": 1234,
        "start_date": "2021-10-08",
        "end_date": "2021-10-11",
        "capacity": 2,
        "options": {
            "parking": 1,
            "baby_cot": 1,
            "romance_pack": 1,
            "breakfast": 1,
        },
    }
    assert utils.book_sanity_check(no_room_json) is False


def test_book_sanity_check_06():
    """check for room capacity."""
    bad_capacity_json = {
        "room_id": 1,
        "start_date": "2021-10-08",
        "end_date": "2021-10-11",
        "capacity": 1234,
        "options": {
            "parking": 1,
            "baby_cot": 1,
            "romance_pack": 1,
            "breakfast": 1,
        },
    }
    assert utils.book_sanity_check(bad_capacity_json) is False


def test_book_sanity_check_07():
    """check for options, make sure all options are an int.
    Check later if they are 0 or 1."""
    bad_options_json = {
        "room_id": 1,
        "start_date": "2021-10-08",
        "end_date": "2021-10-11",
        "capacity": 2,
        "options": {
            "hello": 1,
            "baby_cot": 1,
            "romance_pack": 1,
            "breakfast": 1,
        },
    }
    assert utils.book_sanity_check(bad_options_json) is False

    del bad_options_json['options']['hello']
    bad_options_json['options']['parking'] = 'hello'

    assert utils.book_sanity_check(bad_options_json) is False
