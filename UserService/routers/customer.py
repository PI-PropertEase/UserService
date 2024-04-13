from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from UserService import crud
from UserService.dependencies import get_user, get_db
from UserService.messaging_operations import publish_new_user, publish_import_properties
from UserService.schemas import UserBase, User, Service, pydantic_service_from_db_service
from UserService.models import Service as ServiceEnum

# deny by default
router = APIRouter(dependencies=[Depends(get_user)])


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    db_user = crud.create_user(db=db, user=user)
    await publish_new_user(user)
    return db_user


@router.post("/services", response_model=User, status_code=status.HTTP_201_CREATED)
async def connect_to_service(
    service: Service, user: UserBase = Depends(get_user), db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if ServiceEnum(service.title.value) in db_user.connected_services:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already connected to that service",
        )
    db_user.connected_services.append(ServiceEnum(service.title.value))
    ret_user = crud.update_user(db=db, updated_user=db_user)

    await publish_import_properties(service.title, user)

    # convert "models.Service[]" type to "schemas.Service[]" type for serialization
    ret_user.connected_services = [
        pydantic_service_from_db_service(db_s) for db_s in ret_user.connected_services
    ]
    return ret_user


@router.get("/users", response_model=User)
def read_user(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user.connected_services = [pydantic_service_from_db_service(db_service) for db_service in db_user.connected_services]
    return db_user


@router.get("/services", response_model=list[Service])
def get_available_services():
    available_services = [Service(title=s.value) for s in ServiceEnum]
    return available_services
