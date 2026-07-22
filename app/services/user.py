import logging as log

from app.models import User
from app.utils import auth, mongo

COLLECTION = "users"


async def find(id_: str = None, email: str = None, include_password: bool = False) -> dict:
    condition = {"_id": id_} if id_ else {"email": email}
    user = await mongo.find_one(COLLECTION, condition)
    exclude = set() if include_password else {"password"}
    return User(**user).model_dump(exclude=exclude)


async def create(user: User) -> dict:
    user.password = auth.hash_password(user.password)
    user = await mongo.create(COLLECTION, user)
    log.info(f"New Record! Collection: {COLLECTION} | Data: {user}")
    return User(**user).model_dump()


async def add_points(email: str, delta: int) -> dict | None:
    condition = {"email": email} if delta >= 0 else {"email": email, "points": {"$gte": -delta}}
    user = await mongo.find_one_and_update(COLLECTION, condition, {"$inc": {"points": delta}})
    return User(**user).model_dump() if user else None
