import datetime
import enum

from faker import Faker
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import Boolean
from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

import sys

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
    conn.execute('CREATE DATABASE IF NOT EXISTS {0}'.format(DB_NAME))


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
    lundi = 0
    mardi = 1
    mercredi = 2
    jeudi = 3
    vendredi = 4
    samedi = 5
    dimanche = 6


class Hostel(Base):
    __tablename__ = "hostel"
    id = Column(Integer, primary_key=True)
    telephone = Column(String(20))
    website = Column(String(100))
    description = Column(String(100))
    owner = Column(String(50))
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey("hostel.id"))
    number = Column(String(50))
    street = Column(String(50))
    town = Column(String(50))
    postal_code = Column(Integer)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey("hostel.id"))
    rooms = Column(Enum(RoomEnum))
    capacity = Column(Integer)
    price = Column(Float)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )


class Customer(Base):
    __tablename__ = "customer"
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
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )


class Booking(Base):
    __tablename__ = "booking"
    id = Column(BigInteger, primary_key=True)
    rooms_id = Column(Integer, ForeignKey("rooms.id"))
    customer_id = Column(BigInteger, ForeignKey("customer.id"))
    order_price = Column(Float)
    booking_start_date = Column(Date)
    booking_end_date = Column(Date)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )


class PricePolicy(Base):
    __tablename__ = 'price_policy'
    id = Column(Integer, primary_key=True)
    rooms_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String(100))
    rooms_majoration = Column(Float)
    day_number = Column(Enum(DayEnum))
    majoration_start_date = Column(DateTime)
    majoration_end_date = Column(DateTime)
    is_default = Column(Boolean, nullable=False)
    created_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )


Hostel.address = relationship(
    "Address", order_by=Address.id, back_populates="hostel", uselist=False,
)
Hostel.rooms = relationship("Rooms", order_by=Rooms.id, back_populates="hostel")
Rooms.booking = relationship("Booking", order_by=Booking.id, back_populates="rooms")
Customer.booking = relationship("Booking", order_by=Booking.id, back_populates="customer")
PricePolicy.rooms = relationship("Rooms", order_by=Rooms.id, back_populates="price_policy")

Base.metadata.create_all(db_engine)


fake = Faker(['fr_FR'])
fake_us = Faker(['en_US'])

# Generate fake data for Hostel
hostel_data = []
for _ in range (2):
    phone = fake.phone_number()
    website = fake.uri()
    description = fake.catch_phrase()
    owner = fake.name()
    row = (phone, website, description, owner)
    hostel_data.append(row)

try:
    query=f"INSERT INTO `hostel` (`telephone`, `website`, `description`, `owner`) VALUES(%s,%s,%s,%s)"
    id=db_engine.execute(query, hostel_data)
except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)

# Generate fake data for Address
address_data = []
i = 0
for _ in range(2):
    i += 1
    hostel_id = i
    number = fake.building_number()
    street = fake.street_name()
    town = fake.city()
    postal_code = fake.postcode()
    row = (hostel_id, number, street, town, postal_code)
    address_data.append(row)

try:
    query=f"INSERT INTO `address` (`hostel_id`, `number`, `street`, `town`, `postal_code`) VALUES(%s,%s,%s,%s,%s)"
    id=db_engine.execute(query, address_data)
except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)

# Generate fake data for Rooms
rooms_data = [(1, 'S', 3, 720),
              (1, 'JS', 2, 500),
              (1, 'CD', 2, 300),
              (1, 'CS', 2, 150),
              (1, 'CS', 2, 150),
              (2, 'SR', 5, 1000),
              (2, 'SR', 5, 1000)]

try:
    query=f"INSERT INTO `rooms` (`hostel_id`, `rooms`, `capacity`, `price`) VALUES(%s,%s,%s,%s)"
    id=db_engine.execute(query, rooms_data)
except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)


# Generate fake data for Customer
customer_data = []
for _ in range(500):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.ascii_free_email()
    telephone = fake.phone_number()
    username = fake_us.simple_profile()['username']
    password = fake_us.password(length=12)
    row = (first_name, last_name, email, telephone, username, password)
    customer_data.append(row)

try:
    query=f"INSERT INTO `customer` (`first_name`, `last_name`, `email`, `telephone`, `username`, `password`) VALUES(%s,%s,%s,%s,%s,%s)"
    id=db_engine.execute(query, customer_data)
except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)

# Generate fake data for Booking
##############
#

# Pour les nuits de vendredi et samedi le prix des chambres est majoré de 15%
# Les nuits du mercredi et jeudi sont minoré de 10%
# Si une seule personne occupe la chambre le prix est minoré de 5%
# Generate fake data for PricePolicy
price_policy_data = [(1, 'Wednesday Majoration', -10, 2, True),
                     (1, 'Thursday Majoration', -10, 3, True),
                     (1, 'Friday Majoration', 15, 4, True),
                     (1, 'Saturday Majoration', 15, 5, True),

                     (2, 'Wednesday Majoration', -10, 2, True),
                     (2, 'Thursday Majoration', -10, 3, True),
                     (2, 'Friday Majoration', 15, 4, True),
                     (2, 'Saturday Majoration', 15, 5, True),
                     
                     (3, 'Wednesday Majoration', -10, 2, True),
                     (3, 'Thursday Majoration', -10, 3, True),
                     (3, 'Friday Majoration', 15, 4, True),
                     (3, 'Saturday Majoration', 15, 5, True),
                     
                     (4, 'Wednesday Majoration', -10, 2, True),
                     (4, 'Thursday Majoration', -10, 3, True),
                     (4, 'Friday Majoration', 15, 4, True),
                     (4, 'Saturday Majoration', 15, 5, True),

                     (5, 'Wednesday Majoration', -10, 2,True),
                     (5, 'Thursday Majoration', -10, 3,True),
                     (5, 'Friday Majoration', 15, 4,True),
                     (5, 'Saturday Majoration', 15, 5,True),

                     (6, 'Wednesday Majoration', -10, 2,True),
                     (6, 'Thursday Majoration', -10, 3,True),
                     (6, 'Friday Majoration', 15, 4,True),
                     (6, 'Saturday Majoration', 15, 5,True),

                     (7, 'Wednesday Majoration', -10, 2,True),
                     (7, 'Thursday Majoration', -10, 3,True),
                     (7, 'Friday Majoration', 15, 4,True),
                     (7, 'Saturday Majoration', 15, 5,True)]



try:
    query=f"INSERT INTO `price_policy` (`rooms_id`, `name`, `rooms_majoration`, `day_number`, `is_default`) VALUES(%s,%s,%s,%s,%s)"
    id=db_engine.execute(query, price_policy_data)
except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
