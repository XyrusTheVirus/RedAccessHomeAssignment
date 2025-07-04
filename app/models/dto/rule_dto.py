from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
