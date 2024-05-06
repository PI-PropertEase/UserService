from sqlalchemy.orm import Session
from sqlalchemy import update
from UserService.schemas import UserBase
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserBase):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()


def update_user(db: Session, updated_user: models.User):
    db.query(models.User).filter(models.User.id == updated_user.id).update(
        {models.User.connected_services: updated_user.connected_services}
    )
    db.commit()
    db.refresh(updated_user)
    return updated_user
