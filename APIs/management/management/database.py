import sqlalchemy
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import delete
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy import update
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
        )
        return options

    def get_hotels(self) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """ Get all hotels with their address. """

        addresses_table = self.setup_addresses_table()
        hotels_table = self.setup_hotels_table()
        join = hotels_table.join(
            addresses_table,
            hotels_table.c.id == addresses_table.c.hotel_id,
        )
        query = select(
            hotels_table.c.id,
            hotels_table.c.name,
            hotels_table.c.telephone,
            hotels_table.c.website,
            hotels_table.c.description,
            hotels_table.c.owner,
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
                hotels_table.c.telephone,
                hotels_table.c.website,
                hotels_table.c.description,
                hotels_table.c.owner,
                addresses_table.c.number,
                addresses_table.c.street,
                addresses_table.c.postal_code,
                addresses_table.c.town,
            )
            .where(hotels_table.c.id == hotel_id)
            .select_from(join)
        )

        # Return the dict, not the list
        return self.engine.connect().execute(query).fetchone()

    def create_hotel(
        self,
        hotel,
    ) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """ Create an hotel and its address. """

        hotel_table = self.setup_hotels_table()

        query_hotel = insert(hotel_table).values(
            name=hotel.name,
            telephone=hotel.telephone,
            website=hotel.website,
            description=hotel.description,
            owner=hotel.owner,
        )

        self.engine.connect().execute(query_hotel)
        last_hotel_id = (
            self.engine.connect()
            .execute(
                "SELECT LAST_INSERT_ID() as id",
            )
            .fetchone()
        )

        return {"id": last_hotel_id.id, **hotel.dict()}

    def update_hotel(self, hotel, hotel_id):
        """ Update hotel by its id. """

        hotel_table = self.setup_hotels_table()

        query = (
            update(hotel_table)
            .values(
                name=hotel.name,
                telephone=hotel.telephone,
                website=hotel.website,
                description=hotel.description,
                owner=hotel.owner,
            )
            .where(hotel_table.c.id == hotel_id)
        )

        self.engine.connect().execute(query)

        return {"id": hotel_id, **hotel.dict()}

    def delete_hotel(self, hotel_id):
        """ Delete hotel by its id. """

        hotel_table = self.setup_hotels_table()

        # TODO : Check if the cascade deletion is up or not ?
        query = delete(hotel_table).where(hotel_table.c.id == hotel_id)

        return self.engine.connect().execute(query).all()

    def get_all_addresses(self):
        """ Get all addresses. """

        address_tables = self.setup_addresses_table()

        query = select(
            address_tables.c.id,
            address_tables.c.hotel_id,
            address_tables.c.number,
            address_tables.c.street,
            address_tables.c.postal_code,
            address_tables.c.town,
        )

        return self.engine.connect().execute(query).all()

    def get_address_by_hotel_id(self, hotel_id):
        """ Return hotel's address, find by hotel's id ."""
        address_table = self.setup_addresses_table()

        query = select(
            address_table.c.id,
            address_table.c.hotel_id,
            address_table.c.number,
            address_table.c.street,
            address_table.c.town,
            address_table.c.postal_code,
        ).where(address_table.c.hotel_id == hotel_id)

        result = self.engine.connect().execute(query).all()
        return result

    def get_address_by_id(self, address_id):
        """ Return address by its id ."""
        address_table = self.setup_addresses_table()

        query = select(
            address_table.c.id,
            address_table.c.hotel_id,
            address_table.c.number,
            address_table.c.street,
            address_table.c.town,
            address_table.c.postal_code,
        ).where(address_table.c.id == address_id)

        result = self.engine.connect().execute(query).fetchone()
        return result

    def create_address(self, address, hotel_id):
        """ Create address. """

        address_table = self.setup_addresses_table()
        query = insert(address_table).values(
            hotel_id=hotel_id,
            number=address.number,
            street=address.street,
            town=address.town,
            postal_code=address.postal_code,
        )

        self.engine.connect().execute(query)
        last_address_id = (
            self.engine.connect()
            .execute(
                "SELECT LAST_INSERT_ID() as id",
            )
            .fetchone()
        )

        return {"id": last_address_id.id, **address.dict()}

    def update_address(self, address, address_id):
        """ Update an address by its id. """

        address_table = self.setup_addresses_table()
        query = insert(address_table).values(
            hotel_id=address.hotel_id,
            number=address.number,
            street=address.street,
            town=address.town,
            postal_code=address.postal_code,
        )

        self.engine.connect().execute(query)
        return {"id": address_id, **address.dict()}

    def delete_address(self, address_id):
        """ Delete an address by its id. """

        address_table = self.setup_addresses_table()
        query = delete(address_table).where(address_table.c.id == address_id)

        return self.engine.connect().execute(query)

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

    def get_options(self) -> sqlalchemy.engine.cursor.LegacyCursorResult:
        """ Get all options. """

        option_table = self.setup_options_table()

        query = select(
            option_table.c.id,
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

        query = insert(option_table).values(
            name=option.name,
            price=option.price,
        )

        self.engine.connect().execute(query)
        last_row = (
            self.engine.connect()
            .execute(
                "SELECT LAST_INSERT_ID() as id",
            )
            .fetchone()
        )

        return {"id": last_row.id, **option.dict()}

    def update_option(self, option, option_id):
        """ Update an option. """

        option_table = self.setup_options_table()

        query = (
            update(option_table)
            .where(option_table.c.id == option_id)
            .values(
                name=option.name,
                price=option.price,
            )
        )

        self.engine.connect().execute(query)
        return {"id": option_id, **option.dict()}

    def delete_option(self, option_id):
        """ Delete an option. """
        option_table = self.setup_options_table()

        query = delete(option_table).where(option_table.c.id == option_id)

        return self.engine.connect().execute(query)

    def get_price_policies(self):
        """ Get all price_policies. """

        pp_table = self.setup_price_policies_table()

        query = select(
            pp_table.c.id,
            pp_table.c.name,
            pp_table.c.room_id,
            pp_table.c.room_majoration,
            pp_table.c.price_policy_type,
            pp_table.c.day_number,
            pp_table.c.capacity_limit,
            pp_table.c.is_default,
            pp_table.c.majoration_start_date,
            pp_table.c.majoration_end_date,
        )

        pp_result = self.engine.connect().execute(query).all()
        return pp_result

    def get_price_policy_by_id(self, price_policy_id):
        """ Get price_policy bi its id. """

        pp_table = self.setup_price_policies_table()

        query = select(
            pp_table.c.id,
            pp_table.c.name,
            pp_table.c.room_id,
            pp_table.c.room_majoration,
            pp_table.c.price_policy_type,
            pp_table.c.day_number,
            pp_table.c.capacity_limit,
            pp_table.c.is_default,
            pp_table.c.majoration_start_date,
            pp_table.c.majoration_end_date,
        ).where(pp_table.c.id == price_policy_id)

        pp_result = self.engine.connect().execute(query).all()
        return pp_result

    def create_price_policy(self, price_policy):
        """ Create a new price_policy. """

        pp_table = self.setup_price_policies_table()

        # TODO : Add check
        # manage_rules_price_policies

        query = insert(pp_table).values(
            name=price_policy.name,
            room_id=price_policy.room_id,
            room_majoration=price_policy.room_majoration,
            price_policy_type=price_policy.price_policy_type,
            day_number=price_policy.day_number,
            capacity_limit=price_policy.capacity_limit,
            is_default=price_policy.is_default,
            majoration_start_date=price_policy.majoration_start_date,
            majoration_end_date=price_policy.majoration_end_date,
        )

        self.engine.connect().execute(query)
        last_row = (
            self.engine.connect()
            .execute(
                "SELECT LAST_INSERT_ID() as id",
            )
            .fetchone()
        )

        return {"id": last_row.id, **price_policy.dict()}

    def update_price_policy(self, price_policy, price_policy_id):
        """ Update an option. """

        pp_table = self.setup_price_policies_table()

        # TODO : Add check
        # manage_rules_price_policies

        query = (
            update(pp_table)
            .where(pp_table.c.id == price_policy_id)
            .values(
                name=price_policy.name,
                room_id=price_policy.room_id,
                price_policy_type=price_policy.price_policy_type,
                room_majoration=price_policy.room_majoration,
                day_number=price_policy.day_number,
                capacity_limit=price_policy.capacity_limit,
                is_default=price_policy.is_default,
                majoration_start_date=price_policy.majoration_start_date,
                majoration_end_date=price_policy.majoration_end_date,
            )
        )

        self.engine.connect().execute(query)
        return {"id": price_policy_id, **price_policy.dict()}

    def delete_price_policy(self, price_policy_id):
        """ Delete an option. """

        pp_table = self.setup_price_policies_table()

        query = delete(pp_table).where(pp_table.c.id == price_policy_id)

        return self.engine.connect().execute(query)
