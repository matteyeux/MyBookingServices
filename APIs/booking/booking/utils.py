from datetime import datetime
from datetime import timedelta


def check_dates(start: str = None, end: str = None) -> bool:
    """Validates if :
    - start_date is equal or after current_date
    - start_date is before end_date
    - start_date is not equal end_date
    - end_date is after current_date + 1 day
    - end_date is after start_date
    """
    if None in [start, end]:
        return False

    current_date = datetime.today()
    start_date = datetime.strptime(str(start), "%Y-%m-%d")
    end_date = datetime.strptime(str(end), "%Y-%m-%d")

    # start date check
    if (
        (current_date > start_date)
        or (end_date < start_date)
        or (start_date == end_date)
    ):
        return False

    # end date check
    if (
        (current_date + timedelta(days=1)) > end_date
    ) or start_date > end_date:
        return False

    return True
