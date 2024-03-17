from pydantic import BaseModel


class Service(BaseModel):
    title: str


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: int
    connected_services: list[Service]
