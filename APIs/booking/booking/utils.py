from datetime import datetime
from datetime import timedelta

import numpy as np
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

    # Create range of date between start date and end date
    df_date = pd.DataFrame()
    sdate = datetime.strptime(booking_data["start_date"], "%Y-%m-%d").date()
    edate = datetime.strptime(booking_data["end_date"], "%Y-%m-%d").date()
    date_range = pd.date_range(sdate, edate - timedelta(days=1), freq="d")

    # room_up = room unit price
    room_up = room[0][4]

    # Divide room_majoration by 100 to calcul majoration properly
    df_pp = pd.DataFrame.from_dict(pp)
    df_pp["room_majoration"] = df_pp["room_majoration"] / 100

    # Create df_pp_day to calcul majoration only day for each day
    df_pp_day = df_pp.loc[df_pp["price_policy_type"] == 1]
    df_pp_day = update_pp_day(df_pp_day, sdate, edate)

    # Create df_pp_capacity to calcul majoration only on capacity for each day
    df_pp_capacity = df_pp.loc[df_pp["price_policy_type"] == 2]
    df_pp_capacity = update_pp_capacity(df_pp_capacity, sdate, edate)

    for e in date_range:
        new_date = {}
        new_date["date"] = e
        new_date["day"] = float(e.strftime("%w"))
        df_date = df_date.append(new_date, ignore_index=True)

    # Merge date range and price policy to set majoration on right dayss
    new_df = df_date.merge(df_pp_day, how="left", on="date").merge(
        df_pp_capacity,
        on="date",
    )
    print(new_df)
    # Calcul final price of room depand on majorations days
    # and majoration capacity
    price = 0
    for index, row in new_df.iterrows():
        if booking_data["capacity"] > row["capacity_limit"]:
            price += room_up + (room_up * row["room_majoration_day"])
        else:
            price += (
                room_up
                + (room_up * row["room_majoration_day"])
                + (room_up * row["room_majoration_capacity"])
            )

    for elem in booking_data["options"]:
        if booking_data["options"][elem]:
            price += booking_data["options"][elem]

    print(price)

    return price


def update_pp_capacity(
    df_pp_capacity: pd.DataFrame,
    sdate: datetime,
    edate: datetime,
) -> pd.DataFrame:
    # Keep only row with value 'is_default' equals to 'False'
    df_tmp = df_pp_capacity.loc[~df_pp_capacity["is_default"]]

    # If there is none value 'False' attribute value
    # sdate to column 'majoration_start_date'
    # edate to column 'majoration_end_date' becarefull
    # if range is over two month
    if len(df_tmp) > 0:
        for index, row in df_tmp.iterrows():
            majoration_sdate = datetime.strptime(
                row["majoration_start_date"],
                "%Y-%m-%d %H:%M:%S",
            ).date()
            majoration_edate = datetime.strptime(
                row["majoration_end_date"],
                "%Y-%m-%d %H:%M:%S",
            ).date()
            if (
                majoration_sdate < sdate < majoration_edate
                or majoration_sdate < edate < majoration_edate
            ):
                if majoration_sdate < sdate:
                    df_tmp.at[index, "majoration_start_date"] = sdate
                else:
                    df_tmp.at[
                        index,
                        "majoration_start_date",
                    ] = majoration_sdate
                if majoration_edate > edate:
                    df_tmp.at[index, "majoration_end_date"] = edate
                else:
                    df_tmp.at[index, "majoration_end_date"] = majoration_edate
            else:
                df_tmp = df_tmp.drop([index])
        if len(df_tmp) > 0:
            # Generate all date between range date
            # 'majoration_start_date' and 'majoration_end_date'
            s = pd.concat(
                pd.Series(
                    r.Index,
                    pd.date_range(
                        r.majoration_start_date,
                        r.majoration_end_date,
                    ),
                )
                for r in df_tmp.itertuples()
            )
            df_pp_capacity = (
                df_tmp.loc[s]
                .assign(
                    date=s.index,
                )
                .reset_index(drop=True)
            )
        else:
            df_pp_capacity = add_rows_range_date(sdate, edate, df_pp_capacity)
    else:
        df_pp_capacity = add_rows_range_date(sdate, edate, df_pp_capacity)

    # drop columns non utils and rename some columns to prepare merging
    df_pp_capacity.drop(
        columns=[
            "price_policy_type",
            "day_number",
            "majoration_start_date",
            "majoration_end_date",
            "is_default",
        ],
        inplace=True,
    )
    df_pp_capacity.rename(
        columns={
            "room_majoration": "room_majoration_capacity",
            "name": "name_capacity",
        },
        inplace=True,
    )
    return df_pp_capacity


def update_pp_day(
    df_pp_day: pd.DataFrame,
    sdate: datetime,
    edate: datetime,
) -> pd.DataFrame:
    # Keep only row with value 'is_default' equals to 'False'
    df_tmp = df_pp_day.loc[~df_pp_day["is_default"]]

    # If there is none value 'False' attribute value
    # sdate to column 'majoration_start_date'
    # edate to column 'majoration_end_date' becarefull
    # if range is over two month
    if len(df_tmp) > 0:
        for index, row in df_tmp.iterrows():
            majoration_sdate = datetime.strptime(
                row["majoration_start_date"],
                "%Y-%m-%d %H:%M:%S",
            ).date()
            majoration_edate = datetime.strptime(
                row["majoration_end_date"],
                "%Y-%m-%d %H:%M:%S",
            ).date()
            if (
                majoration_sdate < sdate < majoration_edate
                or majoration_sdate < edate < majoration_edate
            ):
                if majoration_sdate < sdate:
                    df_tmp.at[index, "majoration_start_date"] = sdate
                else:
                    df_tmp.at[
                        index,
                        "majoration_start_date",
                    ] = majoration_sdate
                if majoration_edate > edate:
                    df_tmp.at[index, "majoration_end_date"] = edate
                else:
                    df_tmp.at[index, "majoration_end_date"] = majoration_edate
            else:
                df_tmp = df_tmp.drop([index])
        if len(df_tmp) > 0:
            # Generate all date between range date 'majoration_start_date'
            # and 'majoration_end_date'
            s = pd.concat(
                pd.Series(
                    r.Index,
                    pd.date_range(
                        r.majoration_start_date,
                        r.majoration_end_date,
                    ),
                )
                for r in df_tmp.itertuples()
            )
            df_pp_day = (
                df_tmp.loc[s]
                .assign(
                    date=s.index,
                )
                .reset_index(drop=True)
            )
        else:
            df_pp_day = add_rows_range_date(sdate, edate, df_pp_day)
    else:
        df_pp_day = add_rows_range_date(sdate, edate, df_pp_day)

    # delete all wrong values
    for index, row in df_pp_day.iterrows():
        if row["day_number"] > 0 and row["day_number"] != float(
            row["date"].strftime("%w"),
        ):
            df_pp_day.at[index, "room_majoration"] = float(0)
            df_pp_day.at[index, "day_number"] = np.nan
    df_pp_day["absolute_maj"] = df_pp_day["room_majoration"].abs()
    df_pp_day.sort_values(by=["absolute_maj"], ascending=False, inplace=True)
    df_pp_day.drop_duplicates(subset=["date"], keep="first", inplace=True)
    df_pp_day.sort_values(by=["date"], ascending=True, inplace=True)

    # drop columns non utils and rename some columns to prepare merging
    df_pp_day.drop(
        columns=[
            "price_policy_type",
            "capacity_limit",
            "majoration_start_date",
            "majoration_end_date",
            "is_default",
            "absolute_maj",
        ],
        inplace=True,
    )
    df_pp_day.rename(
        columns={
            "room_majoration": "room_majoration_day",
            "name": "name_day",
        },
        inplace=True,
    )
    print(df_pp_day)

    return df_pp_day


def add_rows_range_date(
    sdate: datetime.date,
    edate: datetime.date,
    df_pp: pd.DataFrame,
) -> pd.DataFrame:

    df_pp = df_pp.loc[df_pp["is_default"]]
    # Generate all date between range date 'sdate' and 'edate'
    s = pd.concat(
        pd.Series(r.Index, pd.date_range(sdate, edate))
        for r in df_pp.itertuples()
    )
    df_pp = df_pp.loc[s].assign(date=s.index).reset_index(drop=True)

    return df_pp


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
