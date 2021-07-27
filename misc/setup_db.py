import datetime
import enum

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
from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import sys

Base = declarative_base()

username = "etna"
password = "etna"
host = "localhost"
# port = 3306
DB_NAME = "mybookingservices"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{DB_NAME}",
)

# with engine.connect() as conn:
#     conn.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")


class RoomEnum(enum.Enum):
    SR = "Suite présidentielle"
    S = "Suite"
    JS = "Junior suite"
    CD = "Chambre de luxe"
    CS = "Chambre standard"


class PolicyEnum(enum.Enum):
    TPM = "temporary"
    PRM = "permanent"


class Hostel(Base):
    __tablename__ = "hostel"
    id = Column(Integer, primary_key=True)
    telephone = Column(Integer)
    website = Column(String(50))
    description = Column(String(50))
    owner = Column(String(50))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey("hostel.id"))
    number = Column(String(50))
    street = Column(String(50))
    town = Column(String(50))
    postal_code = Column(Integer)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey("hostel.id"))
    rooms = Column(Enum(RoomEnum))
    capacity = Column(Integer)
    price = Column(Float)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class Customer(Base):
    __tablename__ = "customer"
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    telephone = Column(Integer)
    username = Column(String(50))
    password = Column(String(50))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class Booking(Base):
    __tablename__ = "booking"
    id = Column(BigInteger, primary_key=True)
    rooms_id = Column(Integer, ForeignKey("rooms.id"))
    customer_id = Column(BigInteger, ForeignKey("customer.id"))
    order_price = Column(Float)
    booking_start_date = Column(Date)
    booking_end_date = Column(Date)
    created_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


# class PricePolicy(Base):
#     __tablename__ = 'price_policy'


Hostel.address = relationship(
    "Address", order_by=Address.id, back_populates="hostel", uselist=False,
)
Hostel.rooms = relationship("Rooms", order_by=Rooms.id, back_populates="hostel")
# TODO add relationship rooms to booking
# TODO add relationship customer to kooking


Base.metadata.create_all(engine)
