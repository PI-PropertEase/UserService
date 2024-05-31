from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from UserService import crud
from UserService.dependencies import get_user, get_db
from UserService.messaging_operations import publish_new_user, publish_import_properties
from UserService.schemas import UserBase, User, Service, pydantic_service_from_db_service
from UserService.models import Service as ServiceEnum

# deny by default
router = APIRouter(dependencies=[Depends(get_user)])


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED,
             summary="Create a new user account", 
             description="Create a new user account, given the bearer token received from Firebase authentication.",
             responses={
                 status.HTTP_201_CREATED: {
                     "description": "Successful Response",
                     "content": {"application/json": {"example": {
                         "email": "user@example.com",
                         "id": 0,
                         "connected_services": []
                     }}}
                 },
                 status.HTTP_400_BAD_REQUEST: {
                     "description": "Email already registered",
                     "content": {"application/json": {"example": {"detail": "Email already registered"}}}
                 }
             })
async def create_user(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    db_user = crud.create_user(db=db, user=user)
    await publish_new_user(user)
    return db_user


@router.post("/services", response_model=User, status_code=status.HTTP_201_CREATED,
             summary="Connect to an external listing service",
             description="Connect to an external listing service, given the service title.",
             responses={
                 status.HTTP_400_BAD_REQUEST: {
                     "description": "User is already connected to that service",
                     "content": {"application/json": {"example": {"detail": "User is already connected to that service"}}}
                 },
                 status.HTTP_404_NOT_FOUND: {
                     "description": "User not found",
                     "content": {"application/json": {"example": {"detail": "User not found"}}}
                 }
             })
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


@router.get("/users", response_model=User,
            summary="Get user account information",
            description="Get user account information, given the bearer token received from Firebase authentication.",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "description": "User not found",
                    "content": {"application/json": {"example": {"detail": "User not found"}}}
                }
            })
def read_user(user: UserBase = Depends(get_user), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user.connected_services = [pydantic_service_from_db_service(db_service) for db_service in db_user.connected_services]
    return db_user


@router.get("/services", response_model=list[Service],
            summary="List all available listing services",
            description="Get a list of all available listing services that can be connected to.",
            responses={
                status.HTTP_200_OK: {
                    "description": "List all available listing services",
                    "content": {"application/json": {"example": [{"title": "zooking"}, {"title": "clickandgo"}, {"title": "earthstayin"}]}}
                }
            })
def get_available_services():
    available_services = [Service(title=s.value) for s in ServiceEnum]
    return available_services
