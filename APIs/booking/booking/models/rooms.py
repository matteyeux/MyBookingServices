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

        available_rooms = self.db.get_available_rooms(
            hotel_id,
            start_date,
            end_date,
            capacity,
        )

        # self.db.get_price_policies(
        #     available_rooms,
        #     start_date,
        #     end_date,
        #     capacity,
        # )

        return available_rooms

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
