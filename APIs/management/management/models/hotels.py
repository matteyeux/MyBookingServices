from management.config import config_api_setup
from management.database import Database


class Hotels:
    """Hotels class model."""

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
        """return the list of all hotels."""

        engine = self.db.engine
        return None if not engine else self.db.get_hotels()

    def get_hotel_by_id(self, hotel_id: int = 1):
        """return the list of all hotels."""

        engine = self.db.engine
        return None if not engine else self.db.get_hotel_by_id(hotel_id)

    def create_hotel(self, hotel):
        """Create an hotel in db and return it."""

        engine = self.db.engine
        return None if not engine else self.db.create_hotel(hotel)

    def update_hotel(self, hotel, hotel_id):
        """ Update hotel by its id. """

        engine = self.db.engine
        return None if not engine else self.db.update_hotel(hotel, hotel_id)

    def delete_hotel(self, hotel_id):
        """ Delete hotel by its id. """

        engine = self.db.engine
        return None if not engine else self.db.delete_hotel(hotel_id)
