from booking import utils


def test_check_dates_01():
    """check dates"""
    start = "2021-09-09"
    end = "2021-09-09"
    assert utils.check_dates(start, end) is False
