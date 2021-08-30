from datetime import datetime
from datetime import timedelta

import pandas as pd
from booking.models.hotels import Hotels
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


def handle_pricing(
    booking_data: dict,
    pp: dict,
    room: dict,
    options: dict,
) -> float:
    """Handle pricing according to some options."""

    # room_up = room unit price
    room_up = room[0][4]

    # Divide room_majoration by 100 to calcul majoration properly
    df_pp = pd.DataFrame.from_dict(pp)
    df_pp['room_majoration'] = df_pp['room_majoration'] / 100

    # Create df_ppf_day to calcul majoration only day for each day
    df_pp_day = df_pp.dropna(subset=['day_number'])

    # Create df_pp_capacity to calcul majoration only on capacity for each day
    df_pp_capacity = df_pp.dropna(subset=['capacity_limit'])

    # Create range of date between start date and end date
    df_date = pd.DataFrame()
    sdate = datetime.strptime(booking_data['start_date'], "%Y-%m-%d").date()
    edate = datetime.strptime(booking_data['end_date'], "%Y-%m-%d").date()

    date_range = pd.date_range(sdate, edate - timedelta(days=1), freq='d')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    for e in date_range:
        new_date = {}
        new_date['date'] = e.strftime("%Y-%m-%d")
        new_date['day'] = float(e.strftime("%w"))
        df_date = df_date.append(new_date, ignore_index=True)

    # Merge date range and price policy to set majoration on right dayss
    new_df = df_date.merge(
        df_pp_day,
        how='left',
        left_on='day',
        right_on='day_number',
    )
    new_df['room_majoration'] = new_df['room_majoration'].fillna(0)

    # Calcul final price of room depand on majorations days
    # and majoration capacity
    price = 0
    capacity_limit = df_pp_capacity.iloc[0]['capacity_limit']
    capacity_maj = df_pp_capacity.iloc[0]['room_majoration']
    for index, row in new_df.iterrows():
        if booking_data['capacity'] > capacity_limit:
            price += room_up + room_up * row['room_majoration']
        else:
            price += (
                room_up
                + room_up * row['room_majoration']
                + room_up * capacity_maj
            )

    # Add options to price
    for elem in booking_data['options']:
        if booking_data['options'][elem]:
            price += options[elem]

    return price


def book_sanity_check(json_data: dict) -> bool:
    """Check if all data sent is ok before handling it."""

    keys = ['hotel_id', 'room_id', 'start_date', 'end_date', 'capacity']
    json_keys = json_data.keys()

    # check if all needed keys are there. No need to look for options yet.
    for key in keys:
        if key not in json_keys:
            print(f"[e] {key} not found")
            return False

    # check hotel_id is not neg
    if json_data['hotel_id'] <= 0:
        print("[e] Cannot use id <= 0")
        return False

    # check if hotel_id exists
    hotels = Hotels()
    hotel = hotels.get_hotel_by_id(json_data['hotel_id'])
    if not hotel:
        print("[e] hotel does not exist")
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
        for key in keys:
            if key not in options_key:
                print(f"[e] option {key} not recognized")
                return False

            if isinstance(json_data['options'][key], int) is False:
                return False

    return True
