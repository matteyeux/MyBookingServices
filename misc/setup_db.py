
import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float, String, Enum, BigInteger, Date, DateTime, TIMESTAMP

Base = declarative_base()

username = 'root'
password = 'root'
host = 'localhost'
# port = 3306
DB_NAME = 'mybookingservices'

engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(username, password, host, DB_NAME))

# with engine.connect() as conn:
#     conn.execute('CREATE DATABASE IF NOT EXISTS {0}'.format(DB_NAME))


class RoomEnum(enum.Enum):
	'SR' = 'Suite présidentielle'
	'S' = 'Suite'
	'JS' = 'Junior suite'
	'CD' = 'Chambre de luxe'
	'CS' = 'Chambre standard'


class PolicyEnum(enum.Enum):
	'TPM' = 'temporary'
	'PRM' = 'permanent'

class Hostel(Base)
	__tablename__ = 'hostel'

	id = Column(Integer, primary_key=True)
	telephone = Column(Integer)
	website = Column(String)
	description = Column(String)
	owner = Column(String)
	created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Address(base):
	__tablename__ = 'address'
	
	id = Column(Integer, primary_key=True)
	hostel_id = Column(Integer, ForeignKey('hostel.id'))
	number = Column(String)
	street = Column(String)
	town = Column(String)
	postal_code = Column(Integer)
	created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Rooms(base):
	__tablename__ = 'rooms'

	id = Column(Integer, primary_key=True)
	hostel_id = Column(Integer, ForeignKey('hostel.id'))
	rooms = Column(Enum(RoomEnum))
	capacity = Column(Integer)
	price = Column(Float)
	created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Customer(Base):
	__tablename__ = 'customer'

	id = Column(BigInteger, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String)
	telephone = Column(Integer)
	username = Column(String)
	password = Column(String)
	created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Booking(base):
	__tablename__ = 'booking'

	id = Column(BigInteger, primary_key=True)
	rooms_id = Column(Integer, ForeignKey('rooms.id'))
	customer_id = Column(BigInteger, ForeignKey('customer.id'))
	order_price = Column(FLoat)
	booking_start_date = Column(Date)
	booking_end_date = Column(Date)
	created_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
	updated_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


# class PricePolicy(Base):
# 	__tablename__ = 'price_policy'



Hostel.address = relationship("Address", order_by = Address.id, back_populates = "hostel", uselist=False)
Hostel.rooms = relationship("Rooms", order_by = Romms.id, back_populates = "hostel")
# TODO add relationship rooms to booking
# TODO add relationship customer to kooking


Base.metadata.create_all(engine)
