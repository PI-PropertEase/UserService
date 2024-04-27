from pydantic import BaseModel, EmailStr
from enum import Enum
from .models import Service as DBService


class AvailableService(str, Enum):
    ZOOKING = "zooking"
    CLICKANDGO = "clickandgo"
    EARTHSTAYIN = "earthstayin"


class Service(BaseModel):
    title: AvailableService


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    id: int
    connected_services: list[Service]


def pydantic_service_from_db_service(db_service: DBService) -> Service:
    return Service(title=db_service.value)
