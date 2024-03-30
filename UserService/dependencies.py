from fastapi import Depends, HTTPException, status, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from ProjectUtils.DecoderService.decode_token import decode_token
from UserService import crud
from UserService.database import SessionLocal
from UserService.schemas import UserBase
from UserService import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(res: Response, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    decoded_token = decode_token(res, cred)
    return UserBase(**decoded_token)


def is_user_admin(res: Response, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
                  db: Session = Depends(get_db)):
    user = get_user(res, cred)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None or db_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
