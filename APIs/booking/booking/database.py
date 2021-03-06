from datetime import datetime

import sqlalchemy
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import insert
from sqlalchemy import delete
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import select


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
        try:
            self.engine = create_engine(self.db_string).connect()
        except sqlalchemy.exc.OperationalError:
            print("could not access database.")
            self.engine = None

    def setup_rooms_table(self) -> sqlalchemy.sql.schema.Table:
        """Setup rooms table."""
        meta = MetaData(self.engine)
        rooms_table = Table(
            "rooms",
            meta,
            Column("id", Integer, primary_key=True),
            Column("hotel_id", Integer, ForeignKey("hotels.id")),
            Column("room", String(50)),
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
        """Setup booking table for database."""
        meta = MetaData(self.engine)
        booking_table = Table(
            "booking",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("room_id", Integer, ForeignKey("rooms.id")),
            Column("user_id", BigInteger, ForeignKey("customers.id")),
            Column("capacity_book", Integer),
            Column("option", JSON),
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
        """Setup hotels table for database."""
        meta = MetaData(self.engine)
        hotels_table = Table(
            "hotels",
            meta,
            Column("id", Integer, primary_key=True),
            Column("name", String(40)),
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

    def setup_addresses_table(self) -> sqlalchemy.sql.schema.Table:
        """Setup addresses table for database."""
        meta = MetaData(self.engine)
        addresses_table = Table(
            "addresses",
            meta,
            Column("id", Integer, primary_key=True),
            Column("hotel_id", Integer, ForeignKey("hotels.id")),
            Column("number", String(50)),
            Column("street", String(50)),
            Column("town", String(50)),
            Column("postal_code", Integer),
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
        return addresses_table

    def setup_price_policies_table(self) -> sqlalchemy.sql.schema.Table:
        """Setup price_policies table for database."""
        meta = MetaData(self.engine)
        price_policies = Table(
            "price_policies",
            meta,
            Column("id", Integer, primary_key=True),
            Column("room_id", Integer, ForeignKey("rooms.id")),
            Column("name", String(100)),
            Column("price_policy_type", Integer),
            Column("room_majoration", Float),
            Column("day_number", Integer),
            Column("capacity_limit", Integer),
            Column("majoration_start_date", DateTime),
            Column("majoration_end_date", DateTime),
            Column("is_default", Boolean, nullable=False),
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
        return price_policies

    def setup_options_table(self) -> sqlalchemy.sql.schema.Table:
        """Setup options table for database."""
        meta = MetaData(self.engine)
        options = Table(
            "options",
            meta,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("price", Float),
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
        return options

    def get_room_by_id(
        self,
        room_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Get room by ID."""
        table = self.setup_rooms_table()
        query = table.select().where(table.c.id == room_id)
        return self.engine.connect().execute(query).all()

    def get_hotels(self) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Get all hotels."""
        addresses_table = self.setup_addresses_table()
        hotels_table = self.setup_hotels_table()
        join = hotels_table.join(
            addresses_table,
            hotels_table.c.id == addresses_table.c.hotel_id,
        )
        query = select(
            hotels_table.c.id,
            hotels_table.c.name,
            addresses_table.c.number,
            addresses_table.c.street,
            addresses_table.c.postal_code,
            addresses_table.c.town,
        ).select_from(join)
        return self.engine.connect().execute(query).all()

    def get_hotel_by_id(
        self,
        hotel_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Get hotel info by ID"""
        addresses_table = self.setup_addresses_table()
        hotels_table = self.setup_hotels_table()
        join = hotels_table.join(
            addresses_table,
            hotels_table.c.id == addresses_table.c.hotel_id,
        )
        query = (
            select(
                hotels_table.c.id,
                hotels_table.c.name,
                addresses_table.c.number,
                addresses_table.c.street,
                addresses_table.c.postal_code,
                addresses_table.c.town,
            )
            .where(hotels_table.c.id == hotel_id)
            .select_from(join)
        )
        return self.engine.connect().execute(query).all()

    def get_all_rooms(
        self,
        hotel_id: int = 0,
        capacity: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """List all rooms in database."""
        rooms_table = self.setup_rooms_table()
        query = select(
            rooms_table.c.id,
            rooms_table.c.hotel_id,
            rooms_table.c.room,
            rooms_table.c.price,
            rooms_table.c.capacity,
        ).where(rooms_table.c.capacity >= capacity)

        if hotel_id > 0:
            query = query.where(rooms_table.c.hotel_id == hotel_id)

        rooms_result = self.engine.connect().execute(query).all()
        rooms = [dict(row) for row in rooms_result]
        return rooms

    def get_booked_rooms_by_hotel(self, hotel_id: int = 1) -> list:
        """Get booked rooms for an hotel."""

        # get all rooms for hotel_id and put data in list
        rooms_table = self.setup_rooms_table()
        query = select(rooms_table.c.id).where(
            rooms_table.c.hotel_id == hotel_id,
        )
        rooms_result = self.engine.connect().execute(query)
        rooms = [room for (room,) in rooms_result]

        # grab the list of booked rooms starting today
        booking = self.setup_booking_table()
        query = select(
            booking.c.room_id,
            booking.c.booking_start_date,
            booking.c.booking_end_date,
        ).where(
            booking.c.room_id.in_(rooms),
            booking.c.booking_end_date > datetime.today(),
        )
        booking_result = self.engine.connect().execute(query).all()

        # we return booked_rooms as a dict
        booked_rooms = [dict(row) for row in booking_result]
        return booked_rooms

    def get_booked_rooms_by_id(self, booking_id: int = 1):
        # grab the booked rooms by id
        booking = self.setup_booking_table()
        query = select(
            booking.c.id,
            booking.c.customer_id
        ).where(booking.c.id == booking_id)

        booking_result = self.engine.connect().execute(query).all()

        return booking_result

    def get_price_policies_for_room(self, room_id: int = 1) -> dict:
        pp_table = self.setup_price_policies_table()

        query = select(
            pp_table.c.name,
            pp_table.c.price_policy_type,
            pp_table.c.room_majoration,
            pp_table.c.day_number,
            pp_table.c.capacity_limit,
            pp_table.c.majoration_start_date,
            pp_table.c.majoration_end_date,
            pp_table.c.is_default,
        ).where(pp_table.c.room_id == room_id)

        prices_result = self.engine.connect().execute(query).all()
        return [dict(row) for row in prices_result]

    def get_options(self) -> list:
        options_table = self.setup_options_table()
        query = select(
            options_table.c.id,
            options_table.c.name,
            options_table.c.price,
        )
        options_result = self.engine.connect().execute(query).all()
        return [dict(row) for row in options_result]

    def insert_reservation_into_db(self, user_id: int, data: list):
        """Insert booking data into db"""
        booking_table = self.setup_booking_table()
        query = insert(booking_table).values(
            room_id=data['room_id'],
            customer_id=user_id,
            capacity_book=data['capacity'],
            option=data['options'],
            order_price=data['price'],
            booking_start_date=data['start_date'],
            booking_end_date=data['end_date'],
        )

        self.engine.connect().execute(query)

    def delete_booked_rooms_by_id(self, booking_id: int):
        """Delete booking row data into db"""
        booking_table = self.setup_booking_table()
        query = delete(booking_table).where(
            booking_table.c.id == booking_id,
        )

        return self.engine.connect().execute(query)
