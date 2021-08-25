from datetime import datetime

from booking.models.rooms import Rooms


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


def handle_pricing() -> float:
    """Handle pricing according to some options."""
    price: int = 0
    return float(price)


def book_sanity_check(json_data: dict) -> bool:
    """Check if all data sent is ok before handling it."""

    keys = ['room_id', 'start_date', 'end_date', 'capacity']
    json_keys = json_data.keys()

    # check if all needed keys are there. No need to look for options yet.
    for key in keys:
        if not key in json_keys:
            print(f"[e] {key} not found")
            return False

    # check dates
    if check_dates(json_data['start_date'], json_data['end_date']) is False:
        print("[e] dates are wrong")
        return False

    # check room is not neg
    if json_data['room_id'] <= 0:
        print("[e] Cannot use id <= 0")
        return False

    # check if room exists
    rooms = Rooms()
    room = rooms.get_room_by_id(json_data['room_id'])
    if not room:
        print("[e] room does not exist")
        return False

    # check room capacity
    if json_data['capacity'] > room[0][3]:
        print("[e] capacity is not ok")
        return False

    # check for options
    if "options" in json_keys:
        keys = ['parking', 'baby_cot', 'romance_pack', 'breakfast']
        options_key = json_data['options'].keys()
        for key in options_key:
            if key not in options_key:
                print(f"[e] option {key} not recognized")
                return False

            if isinstance(json_data['options'][key], int) is False:
                return False

    return True
