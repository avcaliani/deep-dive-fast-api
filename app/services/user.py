import logging as log

from app.models import User
from app.utils import auth, mongo

COLLECTION = "users"


async def find(id_: str = None, email: str = None, include_password: bool = False) -> dict | None:
    condition = {"_id": id_} if id_ else {"email": email}
    user = await mongo.find_one(COLLECTION, condition)
    if user is None:
        return None
    exclude = set() if include_password else {"password"}
    return User(**user).model_dump(exclude=exclude)


async def create(user: User) -> dict:
    user.password = auth.hash_password(user.password)
    user = await mongo.create(COLLECTION, user)
    log.info(f"New Record! Collection: {COLLECTION} | Data: {user}")
    return User(**user).model_dump()


async def earn_points(email: str, amount: int) -> dict | None:
    return await _adjust_points(email, amount)


async def spend_points(email: str, cost: int) -> dict | None:
    return await _adjust_points(email, -cost)


async def _adjust_points(email: str, delta: int) -> dict | None:
    should_add_points = delta >= 0
    condition = {"email": email} if should_add_points else {"email": email, "points": {"$gte": -delta}}
    user = await mongo.find_one_and_update(
        collection=COLLECTION, condition=condition, update={"$inc": {"points": delta}}
    )
    return User(**user).model_dump() if user else None
