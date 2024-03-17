import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import customer, admin

cred = credentials.Certificate(".secret.json")
firebase_admin.initialize_app(cred)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(customer.router, tags=["cust"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
