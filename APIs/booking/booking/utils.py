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


def compute_available_rooms(
    rooms: dict,
    reservations: dict,
    start_date: str,
    end_date: str,
) -> list:
    """returns available rooms with correct price etc..."""

    # convert dates
    sdate = datetime.strptime(start_date, "%Y-%m-%d").date()
    edate = datetime.strptime(end_date, "%Y-%m-%d").date()
    available_rooms = []

    for room in rooms:
        if room['id'] not in [resa['room_id'] for resa in reservations]:
            available_rooms.append(room)

        for resa in reservations:
            if (
                resa['room_id'] == room['id']
                and not sdate < resa['booking_start_date'] < edate
                and not sdate < resa['booking_end_date'] < edate
            ):
                available_rooms.append(room)

    return available_rooms


# def handle_pricing() -> str:
#     """Handle pricing according to some options."""
#     price: str = None

#     return price
