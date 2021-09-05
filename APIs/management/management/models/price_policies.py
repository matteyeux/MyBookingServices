from management.config import config_api_setup
from management.database import Database


class Price_Policies:
    """price_policies class model."""

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

    def get_all_price_policies(self):
        """ Return the list of all price_policies. """
        engine = self.db.engine
        return None if not engine else self.db.get_price_policies()

    def get_price_policy_by_id(self, price_policy_id: int = 1):
        """ Return price_policy by its id. """

        engine = self.db.engine
        if not engine:
            return None
        else:
            return self.db.get_price_policy_by_id(price_policy_id)

    def add_price_policy(self, price_policy):
        """Get some information in argument (body, dict, tuple,  ???)
        And add a new price_policy
        """

        engine = self.db.engine
        if not engine:
            return None
        else:
            return self.db.create_price_policy(price_policy)

    def update_price_policy(self, price_policy, price_policy_id):
        """ Update an price_policy given by its id. """
        engine = self.db.engine
        if not engine:
            return None
        else:
            return self.db.update_price_policy(price_policy, price_policy_id)

    def delete_price_policy(self, price_policy_id):
        """ Delete an price_policy given by its id. """
        engine = self.db.engine
        if not engine:
            return None
        else:
            return self.db.delete_price_policy(price_policy_id)
