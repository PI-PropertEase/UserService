from pydantic import BaseModel


class Service(BaseModel):
    title: str


class UserBase(BaseModel):
    email: str


class User(UserBase):
    connected_services: list[Service]
