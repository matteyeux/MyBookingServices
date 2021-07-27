from booking.config import config_api_setup
from booking.database import Database


class Book:
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

    def get_available_rooms(self):
        """Get available rooms to book."""
        engine = self.db.engine
        return None if not engine else self.db.get_available_rooms()
