from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from app.config import settings

MONGODB_CONFIG = settings.MONGODB_CONFIG
DATABASE = settings.MONGODB_DATABASE


class MongoFacade:
    @property
    def url(self) -> str:
        return (
            "mongodb://"
            f"{MONGODB_CONFIG['user']}:{MONGODB_CONFIG['password']}"
            "@"
            f"{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}"
            f"/{DATABASE}"
        )

    def __init__(self):
        self.db = AsyncIOMotorClient(self.url)[DATABASE]

    async def find_one(self, collection: str, condition: dict) -> dict:
        """Return `collection` record filtered by ID.

        Args:
            collection (str): MongoDB collection name.
            condition (dict): Search condition(s).

        Returns:
            dict: Collection Record.
        """
        return await self.db[collection].find_one(condition)

    async def create(self, collection: str, data: BaseModel) -> dict:
        """Create new record into the specified `collection`.

        Args:
            collection (str): MongoDB collection name.
            data (BaseModel): Pydantic Model.

        Returns:
            dict: Created Record.
        """
        new_record = await self.db[collection].insert_one(jsonable_encoder(data))
        new_record = await self.find_one(collection, {"id_": new_record.inserted_id})
        return new_record


mongo = MongoFacade()
