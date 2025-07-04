from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from models.dto import RuleCreate, RuleUpdate
from models import RuleInDB
from dependencies import get_mongo_service
from databases.mongo import MongoService
from fastapi import Depends

class RuleRepository:
    def __init__(self, mongo: MongoService = Depends(get_mongo_service)):
        self.collection = mongo.get_db().get_collection("rules")

    async def create(self, data: dict) -> RuleInDB:
        result = await self.collection.insert_one(data)
        return await self.get(str(result.inserted_id))

    async def get(self, id: str) -> RuleInDB | None:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return RuleInDB(**doc) if doc else None

    async def update(self, id: str, data: RuleUpdate) -> RuleInDB | None:
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return await self.get(id)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0