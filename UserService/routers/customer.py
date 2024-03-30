from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from UserService import crud
from UserService.dependencies import get_user, get_db
from UserService.messaging_operations import publish_new_user
from ProjectUtils.MessagingService.user_schemas import UserBase, User

# deny by default
router = APIRouter(dependencies=[Depends(get_user)])


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)
    publish_new_user(user)
    return db_user


@router.get("/users", response_model=User)
def read_user(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
