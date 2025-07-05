from bson import ObjectId
from databases.mongo import MongoService
from decorators.audit_decorator import audit_action
from dependencies import get_mongo_service
from fastapi import Depends
from models import Rule
from models.dto import RuleCreate, RuleUpdate
from services.audit_emitter import AuditLogger


class RuleRepository:
    def __init__(self, mongo: MongoService = Depends(get_mongo_service)):
        self.collection = mongo.get_db().get_collection("rules")
        self.customer_collection = mongo.get_db().get_collection("rules")
        self.audit = AuditLogger(user="admin")

    @audit_action("create")
    async def create(self, data: dict) -> Rule | None:
        """
        :param data:  dict
        :return: Rule
        """
        result = await self.collection.insert_one(data)
        return await self.get(str(result.inserted_id))

    @audit_action("update")
    async def get(self, id: str) -> Rule | None:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return Rule(**doc) if doc else None

    async def update(self, id: str, data: RuleUpdate) -> Rule | None:
        """
        :param id:  str
        :param data:  RuleUpdate
        :return: Rule | None
        """
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return await self.get(id)

    @audit_action("delete")
    async def delete(self, id: str) -> bool:
        """
        :param id: str
        :return: bool
        """
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
