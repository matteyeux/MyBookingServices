import enum

from faker import Faker
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
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

username = "root"
password = "root"
host = "localhost"
# port = 3306
DB_NAME = "mybookingservices"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/",
)

with engine.connect() as conn:
    conn.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")


db_engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{DB_NAME}",
)


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


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    telephone = Column(String(20))
    website = Column(String(100))
    description = Column(String(100))
    owner = Column(String(50))
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class Addresses(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    number = Column(String(50))
    street = Column(String(50))
    town = Column(String(50))
    postal_code = Column(Integer)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room = Column(Enum(RoomEnum))
    capacity = Column(Integer)
    price = Column(Float)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class Customers(Base):
    __tablename__ = "customers"
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    telephone = Column(String(20))
    username = Column(String(50))
    password = Column(String(50))
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class Booking(Base):
    __tablename__ = "booking"
    id = Column(BigInteger, primary_key=True)
    rooms_id = Column(Integer, ForeignKey("rooms.id"))
    customer_id = Column(BigInteger, ForeignKey("customers.id"))
    capacity_book = Column(Integer)
    order_price = Column(Float)
    booking_start_date = Column(Date)
    booking_end_date = Column(Date)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class PricePolicies(Base):
    __tablename__ = "price_policies"
    id = Column(Integer, primary_key=True)
    rooms_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String(100))
    price_policy_type = Column(Enum(PPTypeEnum))
    rooms_majoration = Column(Float)
    day_number = Column(Enum(DayEnum))
    capacity_limit = Column(Integer)
    majoration_start_date = Column(DateTime)
    majoration_end_date = Column(DateTime)
    is_default = Column(Boolean, nullable=False)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


# Place de garage (25$)
# Ajout d'un lit bébé (sans frais additionnels)
# Pack romance (50$), doit être réservé avec deux jours d'avance
# Petit déjeuner (30$)
class Options(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(float)


Hotels.addresses = relationship(
    "Addresses",
    order_by=Addresses.id,
    back_populates="hotels",
    uselist=False,
)
Hotels.rooms = relationship(
    "Rooms",
    order_by=Rooms.id,
    back_populates="hotels",
)
Rooms.booking = relationship(
    "Booking",
    order_by=Booking.id,
    back_populates="rooms",
)
Customers.booking = relationship(
    "Booking",
    order_by=Booking.id,
    back_populates="customers",
)
PricePolicies.rooms = relationship(
    "Rooms",
    order_by=Rooms.id,
    back_populates="price_policies",
)

Base.metadata.create_all(db_engine)


fake = Faker(["fr_FR"])
fake_us = Faker(["en_US"])

# Generate fake data for Hotel
hotel_data = []
for _ in range(2):
    phone = fake.phone_number()
    website = fake.uri()
    description = fake.catch_phrase()
    owner = fake.name()
    row = (phone, website, description, owner)
    hotel_data.append(row)

try:
    print("[+] inserting data into hotels table")
    query = "INSERT INTO `hotels` (`telephone`, `website`, `description`, \
            `owner`) VALUES( % s, % s, % s, % s)"
    id = db_engine.execute(query, hotel_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Address
address_data = []
for i in range(1, 2):
    hotel_id = i
    number = fake.building_number()
    street = fake.street_name()
    town = fake.city()
    postal_code = fake.postcode()
    row = (hotel_id, number, street, town, postal_code)
    address_data.append(row)

try:
    print("[+] inserting data into addresses table")
    query = "INSERT INTO `addresses` (`hotel_id`, `number`, `street`, \
            `town`, `postal_code`) VALUES(%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, address_data)
except SQLAlchemyError as e:
    print(query)
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Rooms
rooms_data = [
    (1, "S", 3, 720),
    (1, "JS", 2, 500),
    (1, "CD", 2, 300),
    (1, "CS", 2, 150),
    (1, "CS", 2, 150),
    (2, "SR", 5, 1000),
    (2, "SR", 5, 1000),
]

try:
    print("[+] inserting data into rooms table")
    query = "INSERT INTO `rooms` (`hotel_id`, `room`, `capacity`, `price`) \
            VALUES(%s,%s,%s,%s)"
    id = db_engine.execute(query, rooms_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)


# Generate fake data for Customer
customer_data = []
for _ in range(500):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.ascii_free_email()
    telephone = fake.phone_number()
    username = fake_us.simple_profile()["username"]
    password = fake_us.password(length=12)
    row = (first_name, last_name, email, telephone, username, password)
    customer_data.append(row)

try:
    print("[+] inserting data into customers table")
    query = "INSERT INTO `customers` (`first_name`, `last_name`, `email`, \
            `telephone`, `username`, `password`) VALUES(%s,%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, customer_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Booking
booking_data = [
    (3, 54, 2, 990, '2021-05-21', '2021-05-24'),
    (7, 138, 5, 2950, '2021-05-14', '2021-05-17'),
    (6, 417, 1, 5795, '2021-07-05', '2121-07-11'),
    (1, 342, 2, 828, '2121-07-16', '2021-07-17'),
    (4, 94, 2, 150, '2021-07-19', '2021-07-20'),
    (2, 224, 2, 450, '2021-07-21', '2021-07-22'),
    (1, 78, 3, 2160, '2021-09-18', '2021-09-20'),
    (4, 19, 2, 135, '2021-09-29', '2021-09-30'),
    (6, 318, 2, 2150, '2021-10-08', '2021-10-10'),
    (3, 241, 3, 270, '2021-10-27', '2021-10-28'),
]

try:
    print("[+] inserting data into customers table")
    query = "INSERT INTO `booking` (`rooms_id`, `customer_id`, `capacity_book`, \
            `order_price`, `booking_start_date`, `booking_end_date`) \
            VALUES(%s,%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, booking_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)


# Pour les nuits de vendredi et samedi le prix des chambres est majoré de 15%
# Les nuits du mercredi et jeudi sont minoré de 10%
# Si une seule personne occupe la chambre le prix est minoré de 5%
# Generate fake data for PricePolicy
price_policy_data = [
    (1, "Wednesday Minoration", 1, -10, 3, True),
    (1, "Thursday Minoration", 1, -10, 4, True),
    (1, "Friday Majoration", 1, 15, 5, True),
    (1, "Saturday Majoration", 1, 15, 6, True),
    (2, "Wednesday Minoration", 1, -10, 3, True),
    (2, "Thursday Minoration", 1, -10, 4, True),
    (2, "Friday Majoration", 1, 15, 5, True),
    (2, "Saturday Majoration", 1, 15, 6, True),
    (3, "Wednesday Minoration", 1, -10, 3, True),
    (3, "Thursday Minoration", 1, -10, 4, True),
    (3, "Friday Majoration", 1, 15, 5, True),
    (3, "Saturday Majoration", 1, 15, 6, True),
    (4, "Wednesday Minoration", 1, -10, 3, True),
    (4, "Thursday Minoration", 1, -10, 4, True),
    (4, "Friday Majoration", 1, 15, 5, True),
    (4, "Saturday Majoration", 1, 15, 6, True),
    (5, "Wednesday Minoration", 1, -10, 3, True),
    (5, "Thursday Minoration", 1, -10, 4, True),
    (5, "Friday Majoration", 1, 15, 5, True),
    (5, "Saturday Majoration", 1, 15, 6, True),
    (6, "Wednesday Minoration", 1, -10, 3, True),
    (6, "Thursday Minoration", 1, -10, 4, True),
    (6, "Friday Majoration", 1, 15, 5, True),
    (6, "Saturday Majoration", 1, 15, 6, True),
    (7, "Wednesday Minoration", 1, -10, 3, True),
    (7, "Thursday Minoration", 1, -10, 4, True),
    (7, "Friday Majoration", 1, 15, 5, True),
    (7, "Saturday Majoration", 1, 15, 6, True),
]


print("[+] inserting data into price_policies")
try:
    query = "INSERT INTO `price_policies` (`rooms_id`, `name`, \
            `rooms_majoration`, `day_number`, `is_default`) \
            VALUES(%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, price_policy_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)


price_policy_data_v2 = [
    (1, "Capacity Minoration", 2, -5, 1, True),
    (2, "Capacity Minoration", 2, -5, 1, True),
    (3, "Capacity Minoration", 2, -5, 1, True),
    (4, "Capacity Minoration", 2, -5, 1, True),
    (5, "Capacity Minoration", 2, -5, 1, True),
    (6, "Capacity Minoration", 2, -5, 1, True),
    (7, "Capacity Minoration", 2, -5, 1, True),
]


print("[+] inserting data into price_policies v2")
try:
    query = "INSERT INTO `price_policies` (`rooms_id`, `name`, \
            `rooms_majoration`, `capacity_limit`, `is_default`) \
            VALUES(%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, price_policy_data_v2)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Options
options_data = [
    ("Parking", 25),
    ("Baby cot", 0),
    ("Romance pack", 50),
    ("Breakfast", 30)
]

try:
    print("[+] inserting data into options table")
    query = "INSERT INTO `options` (`name`, `price`) \
            VALUES(%s,%s)"
    id = db_engine.execute(query, options_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)
