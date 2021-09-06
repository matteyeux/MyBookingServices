from management.config import config_api_setup
from management.database import Database


class Addresses:
    """Addresses class model."""

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

    def get_all_addresses(self):
        """return the list of all addresses."""

        engine = self.db.engine
        return None if not engine else self.db.get_all_addresses()

    def get_address_by_id(self, address_id: int = 1):
        """return the list of all addresses."""

        engine = self.db.engine
        return None if not engine else self.db.get_address_by_id(address_id)

    def create_address(self, address, hotel_id):
        """Create an address in db and return it."""

        engine = self.db.engine
        return (
            None if not engine else self.db.create_address(address, hotel_id)
        )

    def update_address(self, address, address_id):
        """ Update address by its id. """

        engine = self.db.engine
        return (
            None if not engine else self.db.update_address(address, address_id)
        )

    def delete_address(self, address_id):
        """ Delete address by its id. """

        engine = self.db.engine
        return None if not engine else self.db.delete_address(address_id)
