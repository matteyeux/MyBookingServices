from management.config import config_api_setup
from management.database import Database


class Options:
    """Options class model."""

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

    def get_all_options(self):
        """ Return the list of all options. """

        engine = self.db.engine
        return None if not engine else self.db.get_options()

    def get_option_by_id(self, option_id: int = 1):
        """ Return option by its id. """

        engine = self.db.engine
        return None if not engine else self.db.get_option_by_id(option_id)

    def add_option(self, option):
        """Get some information in argument (body, dict, tuple,  ???)
        And add a new option
        """

        engine = self.db.engine
        return None if not engine else self.db.create_option(option)

    def update_option(self, option, option_id):
        """ Update an option given by its id. """
        engine = self.db.engine
        return None if not engine else self.db.update_option(option, option_id)

    def delete_option(self, option_id):
        """ Delete an option given by its id. """
        engine = self.db.engine
        return None if not engine else self.db.delete_option(option_id)
