import enum
from datetime import datetime
from datetime import timedelta

import sqlalchemy
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy import between
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import not_
from sqlalchemy import or_
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import join


class Database:
    """Database class is used to handle requests to our database."""

    def __init__(
        self,
        connector: str = "mysql+pymysql",
        user: str = None,
        password: str = None,
        host: str = None,
        database: str = None,
    ):
        """Initialize self. See help(type(self)) for accurate signature."""
        self.db_string = f"{connector}://{user}:{password}@{host}/{database}"
        try:
            self.engine = create_engine(self.db_string).connect()
        except sqlalchemy.exc.OperationalError:
            print("could not access database.")
            self.engine = None

    def setup_users_table(self) -> sqlalchemy.sql.schema.Table:
        """Setup users table."""
        meta = MetaData(self.engine)
        users_table = Table(
            "customers",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("first_name", String(50)),
            Column("last_name", String(50)),
            Column("email", String(50)),
            Column("telephone", String(20)),
            Column("username", String(20)),
            Column("password", String(20)),
            Column(
                "created_time",
                TIMESTAMP,
                server_default=text("CURRENT_TIMESTAMP"),
            ),
            Column(
                "updated_time",
                TIMESTAMP,
                server_default=text(
                    "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
                ),
            ),
        )

        return users_table


    def get_all_users(
        self,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """List all users in database."""
        users_table = self.setup_users_table()
        query = select(
            users_table.c.id,
            users_table.c.first_name,
            users_table.c.last_name,
            users_table.c.email,
            users_table.c.telephone,
            users_table.c.username,
            users_table.c.created_time,
            users_table.c.updated_time,
        )

        users_result = self.engine.connect().execute(query).all()

        return users_result


    def get_user_by_id(
        self,
        user_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Get user by ID."""
        table = self.setup_users_table()
        query = table.select().where(table.c.id == user_id)
        return self.engine.connect().execute(query).all()
