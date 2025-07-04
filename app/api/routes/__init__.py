from fastapi import APIRouter
from ..controllers.rules_controller import router as rule_router

api_router = APIRouter()
api_router.include_router(rule_router)