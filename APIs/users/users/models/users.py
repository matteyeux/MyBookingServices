from users.config import config_api_setup
from users.database import Database

class Users:
    """User class model."""

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
    

    def get_all_users(self):
        """Return all users."""
        engine = self.db.engine
        return (
            None if not engine else self.db.get_all_users()
        )