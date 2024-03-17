from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as EnumType
from .database import Base


class Service(EnumType):
    AIRBNB = "airbnb"
    BOOKING = "booking"


class UserRole(EnumType):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    connected_services = Column(ARRAY(Enum(Service)), default=[])
    # is_active = Column(Boolean, default=True) # Do we need this?
