from typing import Union, Literal

from bson import ObjectId
from models.dto.rule_dto import RuleCreate, RuleUpdate
from pydantic import BaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not v:
            return None
        return str(v) if isinstance(v, ObjectId) else str(ObjectId(v))


class RuleDeleteBatch(BaseModel):
    id: PyObjectId


class RuleUpdateBatch(RuleUpdate):
    id: PyObjectId


class RuleBatchItem(BaseModel):
    operation: Literal["create", "update", "delete"]
    data: Union[RuleCreate, RuleUpdateBatch, RuleDeleteBatch]
