from datetime import datetime
from datetime import timedelta

import requests
from fastapi import HTTPException


users_api = "http://localhost:5555"


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


# def handle_pricing() -> str:
#     """Handle pricing according to some options."""
#     price: str = None

#     return price


def user_logged(bearer: str):
    user_logged = requests.get(
        users_api + "/users/me",
        headers={
            "Authorization": bearer,
        },
    )

    if user_logged.status_code == 200:
        return user_logged.json()

    raise HTTPException(status_code=401, detail="User must log in")


def user_is_admin(user: dict):
    if user["role"] == "ADMIN":
        return True

    raise HTTPException(status_code=403, detail="User unauthorised")
