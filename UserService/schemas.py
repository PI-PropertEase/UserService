from pydantic import BaseModel, EmailStr
from enum import Enum


class AvailableService(str, Enum):
    ZOOKING = "zooking"


class Service(BaseModel):
    title: AvailableService


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    id: int
    connected_services: list[Service]
