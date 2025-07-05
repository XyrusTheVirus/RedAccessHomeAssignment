from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any
import os


class MongoService:
    def __init__(self, uri: str = None, db_name: str = None):
        self._uri = uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self._db_name = db_name or os.getenv("MONGO_DB", "app")
        self._client = AsyncIOMotorClient(self._uri)
        self._db = self._client[self._db_name]

    def get_db(self) -> Any:
        return self._db

    def get_collection(self, name: str):
        return self._db[name]
