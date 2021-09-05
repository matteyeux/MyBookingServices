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
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update

from sqlalchemy.sql import select
from sqlalchemy.sql.expression import delete, join


class RoomEnum(enum.Enum):
    SR = "Suite présidentielle"
    S = "Suite"
    JS = "Junior suite"
    CD = "Chambre de luxe"
    CS = "Chambre standard"


class DayEnum(enum.Enum):
    dimanche = 0
    lundi = 1
    mardi = 2
    mercredi = 3
    jeudi = 4
    vendredi = 5
    samedi = 6


class PPTypeEnum(enum.Enum):
    price_policy_days = 1
    price_policy_capacity = 2


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
            self.engine = None

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
        """Setup booking table for database."""
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
            Column("rooms_majoration", Float),
            Column("price_policy_type", Enum(PPTypeEnum)),
            Column("day_number", Enum(DayEnum)),
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
        options= Table(
            "options",
            meta,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("price", Float),
        )
        return options

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

    def create_hotel(
        self,
        hotel,
        address
        ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Create an hotel"""

        return None

    def get_all_rooms(
        self,
        hotel_id: int = 0,
        capacity: int = 0,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """List all rooms in database."""
        rooms_table = self.setup_rooms_table()
        query = select(
            rooms_table.c.id,
            rooms_table.c.hotel_id,
            rooms_table.c.room,
            rooms_table.c.price,
            rooms_table.c.capacity,
        )

        if hotel_id > 0:
            query = query.where(rooms_table.c.hotel_id == hotel_id)

        if capacity > 0:
            query = query.where(rooms_table.c.capacity == capacity)
        rooms_result = self.engine.connect().execute(query).all()

        return rooms_result

    def get_room_by_id(
        self,
        room_id: int = 1,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """Get room by ID."""
        table = self.setup_rooms_table()
        query = table.select().where(table.c.id == room_id)
        return self.engine.connect().execute(query).all()

    def get_price_policies(
        self,
        rooms_result: sqlalchemy.engine.cursor.LegacyCursorResult,
        start_date: str = None,
        end_date: str = None,
        capacity: int = 0,
    ):
        """Get all price policies."""

        # add room_ids in list
        room_ids = []
        for data in rooms_result:
            room_ids.append(data[0])

        pp_table = self.setup_price_policies_table()
        query = select(
            pp_table.c.room_id,
            pp_table.c.rooms_majoration,
            pp_table.c.day_number,
            pp_table.c.is_default,
        ).where(pp_table.c.room_id.in_(room_ids))
        pp_result = jsonable_encoder(
            self.engine.connect().execute(query).all(),
        )

        # json_compatible_item_data = jsonable_encoder(pp_result)
        import pprint

        # print(pp_result)
        pprint.pp(pp_result)
        # print({"available_rooms": pp_result})


    ###############
    ### OPTIONS ###
    ###############
    def get_options(self) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """ Get all options. """

        option_table = self.setup_options_table()

        query = select(
            option_table.c.name,
            option_table.c.price,
        )

        options_result = self.engine.connect().execute(query).all()
        return options_result

    def get_option_by_id(self, option_id: int = 1):
        """ Get option by its id. """
        option_table = self.setup_options_table()

        query = option_table.select().where(option_table.c.id == option_id)
        return self.engine.connect().execute(query).all()

    def create_option(self, option):
        """ Create a new option. """
        option_table = self.setup_options_table()

        query = (
            insert(option_table).
            values(
                name = option.name,
                price = option.price
            )
        )
        
        self.engine.connect().execute(query)
        last_row = self.engine.connect().execute("SELECT LAST_INSERT_ID() as id").fetchone()

        return {**option.dict(), "id": last_row.id}


    def update_option(self, option, option_id):
        """ Update an option. """
        option_table = self.setup_options_table()

        query = (
            update(option_table).
            where(option_table.c.id == option_id).
            values(
                name = option.name,
                price = option.price
            )
        )
        
        self.engine.connect().execute(query)
        return {**option.dict(), "id": option_id}

    def delete_option(self, option_id):
        """ Delete an option. """
        option_table = self.setup_options_table()

        query = (
                delete(option_table).
                where(option_table.c.id == option_id)
        )

        return self.engine.connect().execute(query)

    ####################
    ### PRICE POLICY ###
    ####################

    def get_price_policies(self):
        """ Get all price_policies. """

        pp_table = self.setup_price_policies_table()

        query = select(
            pp_table.c.name,
            pp_table.c.room_majoration,
            pp_table.c.day_number,
            pp_table.c.capacity_limit,
            pp_table.c.is_default,
        )

        # Va falloir faire des jointures

        pp_result = self.engine.connect().execute(query).all()
        return pp_result


    def get_price_policies_by_id(self, price_policy_id):
        """ Get price_policy bi its id. """

        pp_table = self.setup_price_policies_table()

        query = select(
            pp_table.c.name,
            pp_table.c.room_majoration,
            pp_table.c.day_number,
            pp_table.c.capacity_limit,
            pp_table.c.is_default,
        ).where(pp_table.c.id == price_policy_id)

        # Va falloir faire des jointures

        pp_result = self.engine.connect().execute(query).all()
        return pp_result

    def create_price_policy(self, price_policy):
        """ Create a new price_policy. """
        pp_table = self.setup_price_policies_table()

        query = (
            insert(pp_table).
            values(
                room_id = price_policy.c.room_id,
                name = price_policy.c.name,
                price_policy_type = price_policy.c.price_policy_type,
                room_majoration = price_policy.c.room_majoration,
                day_number = price_policy.c.day_number,
                capacity_limit = price_policy.c.capacity_limit,
                is_default = price_policy.c.is_default,
            )
        )
        
        self.engine.connect().execute(query)
        last_row = self.engine.connect().execute("SELECT LAST_INSERT_ID() as id").fetchone()

        return {**price_policy.dict(), "id": last_row.id}

    def update_price_policy(self, price_policy, price_policy_id):
        """ Update an option. """
        pp_table = self.setup_price_policies_table()

        query = (
            update(pp_table).
            where(pp_table.c.id == price_policy_id).
            values(
                room_id = price_policy.c.room_id,
                name = price_policy.c.name,
                price_policy_type = price_policy.c.price_policy_type,
                room_majoration = price_policy.c.room_majoration,
                day_number = price_policy.c.day_number,
                capacity_limit = price_policy.c.capacity_limit,
                is_default = price_policy.c.is_default,
            )
        )
        
        self.engine.connect().execute(query)
        return {**price_policy.dict(), "id": price_policy_id}

    def delete_price_policy(self, price_policy_id):
        """ Delete an option. """
        pp_table = self.setup_price_policies_table()

        query = (
                delete(pp_table).
                where(pp_table.c.id == price_policy_id)
        )

        return self.engine.connect().execute(query)