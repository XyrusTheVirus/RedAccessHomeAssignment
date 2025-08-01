from datetime import datetime
from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        return v if isinstance(v, ObjectId) else ObjectId(v)


class RuleCreate(BaseModel):
    name: str
    description: str
    ip: str
    expired_date: Optional[datetime] = None


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ip: Optional[str] = None
    expired_date: Optional[datetime] = None
