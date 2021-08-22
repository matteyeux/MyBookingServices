from datetime import datetime

from booking.config import config_api_setup
from booking.database import Database


class Rooms:
    """Rooms class model."""

    def __init__(self):
        config, config_file = config_api_setup()
        config.read(config_file)
        self.db = Database(
            connector=config['database']['connector'],
            user=config['database']['user'],
            password=config['database']['password'],
            host=config['database']['host'],
            database=config['database']['database'],
        )

    def compute_available_rooms(
        self,
        rooms: dict,
        reservations: dict,
        start_date: str,
        end_date: str,
    ) -> dict:
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

    def get_available_rooms(
        self,
        hotel_id: int = 1,
        start_date: str = None,
        end_date: str = None,
        capacity: int = 0,
    ):
        """Get available rooms from an hotel for a specific period."""
        if self.db.engine is None:
            print("[e] could not setup database engine")

        # check if dates are not None
        if None in [start_date, end_date]:
            print("dates are None")
            return None

        rooms = self.db.get_all_rooms(hotel_id, capacity)
        reservations = self.db.get_booked_rooms_by_hotel()
        available = self.compute_available_rooms(
            rooms,
            reservations,
            start_date,
            end_date,
        )
        return available

    def get_all_rooms(self, hotel_id: int = 0, capacity: int = 0):
        """Return all rooms."""
        engine = self.db.engine
        return (
            None if not engine else self.db.get_all_rooms(hotel_id, capacity)
        )

    def get_room_by_id(self, room_id: int = 1):
        """Get room info by ID."""
        # if room_id == 0 get latest added room ?
        engine = self.db.engine
        return None if not engine else self.db.get_room_by_id(room_id)
