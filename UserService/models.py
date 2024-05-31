from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as EnumType
from .database import Base


class Service(EnumType):
    ZOOKING = "zooking"
    CLICKANDGO = "clickandgo"
    EARTHSTAYIN = "earthstayin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    connected_services = Column(ARRAY(Enum(Service)), default=[])
