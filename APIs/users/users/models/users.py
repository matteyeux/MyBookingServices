from users.config import config_api_setup
from users.database import Database
from users.models.auth import UserSignupSchema


class Users:
    """User class model."""

    def __init__(self):
        config, config_file = config_api_setup()
        config.read(config_file)
        self.db = Database(
            connector=config["database"]["connector"],
            user=config["database"]["user"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            database=config["database"]["database"],
        )

    def get_all_users(self):
        """Return all users."""
        engine = self.db.engine
        return None if not engine else self.db.get_all_users()

    def get_user_by_id(self, user_id: int):
        engine = self.db.engine
        return None if not engine else self.db.get_user_by_id(user_id)

    def get_user_by_mail(self, user_mail: int):
        engine = self.db.engine
        return None if not engine else self.db.get_user_by_mail(user_mail)

    def create_user(self, user: UserSignupSchema):
        engine = self.db.engine
        return None if not engine else self.db.create_user(user)

    def check_user_login(self, user_mail: str, user_passwd: str):
        user_db = self.get_user_by_mail(user_mail)
        if user_db is not None:
            if user_db.password == user_passwd:
                return user_db
        return None
