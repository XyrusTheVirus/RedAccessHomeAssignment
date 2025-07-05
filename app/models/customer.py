from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return v if isinstance(v, ObjectId) else ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Customer(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    request_rate_limit: int

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        orm_mode = True
