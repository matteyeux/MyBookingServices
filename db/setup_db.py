import datetime
import enum
import hashlib

import pandas as pd
from faker import Faker
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

username = "etna"
password = "etna"
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
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6


class PPTypeEnum(enum.Enum):
    price_policy_days = 1
    price_policy_capacity = 2


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
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
    room = Column(String(50))
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


class Users(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(String(10))
    email = Column(String(50))
    telephone = Column(String(20))
    username = Column(String(50))
    password = Column(String(70))
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
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(BigInteger, ForeignKey("users.id"))
    capacity_book = Column(Integer)
    option = Column(JSON)
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
    room_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String(100))
    price_policy_type = Column(Integer)
    room_majoration = Column(Float)
    day_number = Column(Integer)
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


class Calendar(Base):
    __tablename__ = "calendar"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    day = Column(Integer)
    day_name = Column(String(50))
    day_week = Column(Integer)
    month_name = Column(String(25))
    month = Column(Integer)
    year = Column(Integer)


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
Users.booking = relationship(
    "Booking",
    order_by=Booking.id,
    back_populates="users",
)
PricePolicies.rooms = relationship(
    "Rooms",
    order_by=Rooms.id,
    back_populates="price_policies",
)

Base.metadata.create_all(db_engine)


fake = Faker(["fr_FR"])
fake_us = Faker(["en_US"])

hotel_names = ['Carlton', 'Lutetia']
# Generate fake data for Hotel
hotel_data = []
for i in range(2):
    name = hotel_names[i]
    phone = fake.phone_number()
    website = fake.uri()
    description = fake.catch_phrase()
    owner = fake.name()
    row = (name, phone, website, description, owner)
    hotel_data.append(row)

try:
    print("[+] inserting data into hotels table")
    query = "INSERT INTO `hotels` (`name`, `telephone`, `website`, `description`, \
            `owner`) VALUES( % s, % s, % s, % s, % s)"
    id = db_engine.execute(query, hotel_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Address
address_data = []
for i in range(1, 3):
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

s = hashlib.sha3_224()
# Generate fake data for user
user_data = []
for i in range(2):
    fake_pass = fake_us.password(length=12)
    print(f"admin{i} password : {fake_pass}")
    sha3_hashed_pass = s.update(fake_pass.encode())
    first_name = fake.first_name()
    last_name = fake.last_name()
    role = 'ADMIN'
    email = f"admin{i}@mybooking.services"
    telephone = fake.phone_number()
    password = s.hexdigest()
    row = (first_name, last_name, role, email, telephone, password)
    user_data.append(row)

for _ in range(498):
    sha3_hashed_pass = s.update(fake_us.password(length=12).encode())
    first_name = fake.first_name()
    last_name = fake.last_name()
    role = 'USER'
    email = fake.ascii_free_email()
    telephone = fake.phone_number()
    password = s.hexdigest()
    row = (first_name, last_name, role, email, telephone, password)
    user_data.append(row)

try:
    print("[+] inserting data into users table")
    query = "INSERT INTO `users` (`first_name`, `last_name`, `role`, `email`, \
            `telephone`, `password`) VALUES(%s,%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, user_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Booking
odb = '{"parking": 1, "baby_cot": 1, "romance_pack": 1, "breakfast": 1}'
booking_data = [
    (3, 54, 2, odb, 1095, '2021-05-21', '2021-05-24'),
    (7, 138, 5, odb, 3055, '2021-05-14', '2021-05-17'),
    (6, 417, 1, odb, 5900, '2021-07-05', '2021-07-11'),
    (1, 342, 2, odb, 933, '2021-07-16', '2021-07-17'),
    (4, 94, 2, odb, 255, '2021-07-19', '2021-07-20'),
    (2, 224, 2, odb, 555, '2021-07-21', '2021-07-22'),
    (1, 78, 3, odb, 2265, '2021-09-18', '2021-09-20'),
    (4, 19, 2, odb, 240, '2021-09-29', '2021-09-30'),
    (6, 318, 2, odb, 2255, '2021-10-08', '2021-10-10'),
    (3, 241, 3, odb, 375, '2021-10-27', '2021-10-28'),
]

try:
    print("[+] inserting data into users table")
    query = "INSERT INTO `booking` (`room_id`, `user_id`, `capacity_book`, \
            `option`, `order_price`, `booking_start_date`, `booking_end_date`) \
            VALUES(%s,%s,%s,%s,%s,%s,%s)"
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
    query = "INSERT INTO `price_policies` (`room_id`, `name`, \
            `price_policy_type`, `room_majoration`, `day_number`, \
            `is_default`) VALUES(%s,%s,%s,%s,%s,%s)"
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
    query = "INSERT INTO `price_policies` (`room_id`, `name`, \
            `price_policy_type`, `room_majoration`, `capacity_limit`, \
            `is_default`) VALUES(%s,%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, price_policy_data_v2)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)

# Generate fake data for Options
options_data = [
    ("Parking", 25),
    ("Baby cot", 0),
    ("Romance pack", 50),
    ("Breakfast", 30),
]

try:
    print("[+] inserting data into options table")
    query = "INSERT INTO `options` (`name`, `price`) \
            VALUES(%s,%s)"
    id = db_engine.execute(query, options_data)
except SQLAlchemyError as e:
    error = str(e.__dict__["orig"])
    print(error)


# Generate Calendar
date_data = []
sdate = datetime.date(2021, 1, 1)
edate = datetime.date(2022, 12, 31)
date_range = pd.date_range(sdate, edate - datetime.timedelta(days=1), freq='d')
for e in date_range:
    date = e.strftime("%Y-%m-%d")
    day = e.strftime("%d")
    day_name = e.strftime("%A")
    day_week = e.strftime("%w")
    month_name = e.strftime("%B")
    month = e.strftime("%m")
    year = e.strftime("%Y")
    row = (date, day, day_name, day_week, month_name, month, year)
    date_data.append(row)

try:
    print("[+] inserting data into calendar table")
    query = "INSERT INTO `calendar` (`date`, `day`, `day_name`, \
            `day_week`, `month_name`, `month`, `year`) \
            VALUES(%s,%s,%s,%s,%s,%s,%s)"
    id = db_engine.execute(query, date_data)
except SQLAlchemyError as e:
    print(query)
    error = str(e.__dict__["orig"])
    print(error)
