import asyncio

from UserService.crud import get_users
from UserService.messaging_operations import publish_import_reservations
from sqlalchemy.orm import Session
from UserService.database import SessionLocal

async def schedule_reservations_import():
    with SessionLocal() as db:
        while True:
            print("schedule_reservations_import")
            all_emails = get_users(db)
            await publish_import_reservations(all_emails)
            await asyncio.sleep(10)