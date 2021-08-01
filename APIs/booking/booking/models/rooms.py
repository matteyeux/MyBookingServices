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

    def get_all_rooms(self):
        """Return all rooms."""
        engine = self.db.engine
        return None if not engine else self.db.get_rooms()

    def get_room_by_id(self, room_id: int = 1):
        """Get room info by ID."""
        # if room_id == 0 get latest added room ?
        engine = self.db.engine
        return None if not engine else self.db.get_room_by_id(room_id)
