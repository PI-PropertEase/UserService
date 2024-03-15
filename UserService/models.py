from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as Enumtype
from .database import Base


class Service(Enumtype):
    AIRBNB = "airbnb"
    BOOKING = "booking"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    hashed_password = Column(String)
    connected_services = Column(ARRAY(Enum(Service)), default=[])
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    # is_active = Column(Boolean, default=True) # Do we need this?
