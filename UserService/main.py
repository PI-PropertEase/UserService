import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI, status, Depends
from UserService.dependencies import get_db
from .database import engine
from . import models
from contextlib import asynccontextmanager
from .routers import customer, admin
from fastapi.middleware.cors import CORSMiddleware
from .messaging_operations import init_publisher
import asyncio
from sqlalchemy.orm import Session
from .scheduled_events import schedule_reservations_import, schedule_properties_import


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    await asyncio.ensure_future(init_publisher(loop))
    asyncio.ensure_future(schedule_reservations_import())
    asyncio.ensure_future(schedule_properties_import())
    yield

cred = credentials.Certificate(".secret.json")
firebase_admin.initialize_app(cred)


models.Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get( "/health", tags=["healthcheck"], summary="Perform a Health Check", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK)
def get_health():
    return {"status": "ok"}

app.include_router(customer.router, tags=["cust"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
