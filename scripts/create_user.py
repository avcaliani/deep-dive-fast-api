# Create the Dwight Schrute demo user used throughout the README and the homepage's
# "Try It Live" widget.
# Requires MongoDB running (`docker-compose up -d`).
#
# uv run python scripts/create_user.py
import asyncio

from app.utils import auth
from app.utils.mongo import mongo
from bson import ObjectId

EMAIL = "dwight@dundermifflin.com"
PASSWORD = "Test1234!"  # pragma: allowlist secret


async def create_user() -> None:
    user = {
        "_id": str(ObjectId()),
        "name": "Dwight Schrute",
        "email": EMAIL,
        "birthdate": "1970-01-20",
        "mood": None,
        "enabled": True,
        "password": auth.hash_password(PASSWORD),
        "points": 30,
    }
    await mongo.db["users"].update_one({"email": EMAIL}, {"$setOnInsert": user}, upsert=True)
    print(f"Created {EMAIL} / {PASSWORD}")


if __name__ == "__main__":
    asyncio.run(create_user())
