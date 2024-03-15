from pydantic import BaseModel


class Service(BaseModel):
    title: str


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str
    phone_number: str


class User(UserBase):
    first_name: str
    last_name: str
    phone_number: str
    connected_services: list[Service]
