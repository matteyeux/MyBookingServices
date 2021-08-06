from booking.config import config_api_setup
from booking.database import Database


class Hotels:
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

    def get_all_hotels(self):
        engine = self.db.engine
        """return the list of all hotels."""
        return None if not engine else self.db.get_hotels()

    def get_hotel_by_id(self, hotel_id: int = 1):
        engine = self.db.engine
        """return the list of all hotels."""
        # return self.db.get_hotel_by_id(hotel_id)
        return None if not engine else self.db.get_hotel_by_id(hotel_id)
