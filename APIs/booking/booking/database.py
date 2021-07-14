import enum
from datetime import datetime

import sqlalchemy
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import SmallInteger
from sqlalchemy import Table


class RoomsEnum(enum.Enum):
    room_one = 1
    room_two = 2
    room_three = 3


class Database:
    """Database class is used to handle requests to our database.
    You can call it and specify some parameters ::
            >>> from database import Database
            >>> db = Database(user="matteyeux", password="pass",
                              host="localhost", database="mydb")
            >>> db.db_string
            'mysql+pymysql://matteyeux:pass@localhost/mydb'
            >>>
    """

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
        self.engine = create_engine(self.db_string)

    def setup_rooms_table(self) -> sqlalchemy.sql.schema.Table:
        """Setup rooms table."""
        meta = MetaData(self.engine)
        rooms_table = Table(
            "rooms",
            meta,
            Column("id", Integer, primary_key=True),
            Column("roomType", SmallInteger, nullable=False),
            Column("capacity", SmallInteger, nullable=False),
            Column("price", Float, nullable=False),
            Column("booked", Boolean, nullable=False),
            Column(
                "created_on",
                DateTime,
                nullable=False,
                default=datetime.now(),
                onupdate=datetime.now(),
            ),
            Column(
                "updated_on",
                DateTime,
                nullable=False,
                default=datetime.now(),
                onupdate=datetime.now(),
            ),
        )
        meta.create_all(self.engine)
        return rooms_table

    def get_rooms(self) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Create user."""
        table = self.setup_rooms_table()
        query = table.select()

        return self.engine.connect().execute(query).all()

    def get_room_by_id(
        self,
        room_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Create user."""
        table = self.setup_rooms_table()
        query = table.select().where(table.c.id == room_id)
        return self.engine.connect().execute(query).all()
