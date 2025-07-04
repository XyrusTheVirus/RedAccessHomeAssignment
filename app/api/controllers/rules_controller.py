from fastapi import APIRouter, Body, HTTPException, Path, Depends
from dependencies import get_mongo_service
from repositories.rule_repository import RuleRepository
from models.rule import RuleInDB
from models.dto.rule_dto import RuleCreate, RuleUpdate
import logging

router = APIRouter(prefix="/customers/{customer_id}/rules", tags=["rules"])

@router.post("/", response_model=RuleInDB)
async def create_rule(customer_id: int = Path(...), payload: RuleCreate = Body(...), db=Depends(get_mongo_service)):
    logging.info("Customer ID", customer_id)
    data = payload.dict()
    data["customer_id"] = customer_id
    repo = RuleRepository(db)
    return await repo.create(data)

@router.put("/{id}", response_model=RuleInDB)
async def update_rule(id: str, data: RuleUpdate, db=Depends(get_mongo_service)):
    repo = RuleRepository(db)
    rule = await repo.update(id, data)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule

@router.delete("/{id}")
async def delete_rule(id: str, db=Depends(get_mongo_service)):
    repo = RuleRepository(db)
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"status": "deleted"}