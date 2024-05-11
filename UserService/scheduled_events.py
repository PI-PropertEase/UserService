import asyncio

from UserService.crud import get_users
from UserService.messaging_operations import publish_import_reservations, publish_scheduled_import_properties
from sqlalchemy.orm import Session
from UserService.database import SessionLocal

async def schedule_reservations_import():
    while True:
        with SessionLocal() as db:
            print("schedule_reservations_import")
            all_emails = get_users(db)
            print(all_emails[0] if len(all_emails) > 0 else "No users found")
            await publish_import_reservations(all_emails)
            await asyncio.sleep(20)


async def schedule_properties_import():
    while True:
        with SessionLocal() as db:
            print("Sending scheduled import properties message...")
            all_emails = get_users(db)
            await publish_scheduled_import_properties(all_emails)
            await asyncio.sleep(41)