import enum

import sqlalchemy
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import TIMESTAMP


class RoomEnum(enum.Enum):
    SR = "Suite présidentielle"
    S = "Suite"
    JS = "Junior suite"
    CD = "Chambre de luxe"
    CS = "Chambre standard"


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
            Column("hotel_id", Integer, ForeignKey("hotels.id")),
            Column("room", Enum(RoomEnum)),
            Column("capacity", Integer),
            Column("price", Float),
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
        return rooms_table

    def setup_booking_table(self) -> sqlalchemy.sql.schema.Table:
        meta = MetaData(self.engine)
        booking_table = Table(
            "booking",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("room_id", Integer, ForeignKey("rooms.id")),
            Column("customer_id", BigInteger, ForeignKey("customers.id")),
            Column("capacity_book", Integer),
            Column("order_price", Float),
            Column("booking_start_date", Date),
            Column("booking_end_date", Date),
            Column(
                "created_time",
                TIMESTAMP,
                nullable=False,
                server_default=text("CURRENT_TIMESTAMP"),
            ),
            Column(
                "updated_time",
                TIMESTAMP,
                nullable=False,
                server_default=text(
                    "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
                ),
            ),
        )
        return booking_table

    def setup_hotels_table(self) -> sqlalchemy.sql.schema.Table:
        meta = MetaData(self.engine)
        hotels_table = Table(
            "hotels",
            meta,
            Column("id", Integer, primary_key=True),
            Column("telephone", String(20)),
            Column("website", String(100)),
            Column("description", String(100)),
            Column("owner", String(50)),
            Column(
                "created_time",
                TIMESTAMP,
                nullable=False,
                server_default=text("CURRENT_TIMESTAMP"),
            ),
            Column(
                "updated_time",
                TIMESTAMP,
                nullable=False,
                server_default=text(
                    "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
                ),
            ),
        )
        return hotels_table

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

    def get_available_rooms(
        self,
        room_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Create user."""
        table = self.setup_rooms_table()
        query = table.select().where(table.c.booked == 0)
        return self.engine.connect().execute(query).all()

    def is_room_available(
        self,
        room_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """"""
        table = self.setup_booking_table()
        query = table.select().where(table.c.room_id == room_id)
        return self.engine.connect().execute(query).all()

    def get_hotels(self) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """get all hotels."""
        table = self.setup_hotels_table()
        query = table.select()
        return self.engine.connect().execute(query).all()
