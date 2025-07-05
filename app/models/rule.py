from datetime import date
from typing import Optional

from bson import ObjectId
from models.dto.rule_dto import PyObjectId
from pydantic import BaseModel, Field


class Rule(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    ip: str
    expired_date: Optional[date] = None
    customer_id: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
