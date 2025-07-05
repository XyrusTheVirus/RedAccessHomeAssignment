import logging

from fastapi import APIRouter, HTTPException, Body, Depends
from dependencies import get_mongo_service
from repositories.rule_repository import RuleRepository
from models.rule import Rule
from models.dto.rule_dto import RuleCreate, RuleUpdate
from models.dto.rule_batch_dto import RuleBatchItem
from api.validators.customer import validate_customer_exists
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/customers/{customer_id}/rules", tags=["rules"])

@router.post("/", response_model=Rule)
async def create_rule(
        customer_id: str = Depends(validate_customer_exists),
        payload: RuleCreate = Body(...),
        db=Depends(get_mongo_service)
):
    """
    :param customer_id:
    :param payload:
    :param db:
    :return:
    """
    data = payload.dict()
    data["customer_id"] = customer_id
    repo = RuleRepository(db)
    return await repo.create(data)

@router.put("/{id}", response_model=Rule)
async def update_rule(
        id: str,
        data: RuleUpdate,
        db=Depends(get_mongo_service),
        customer_id: str = Depends(validate_customer_exists)
):
    """
    :param id:
    :param data:
    :param db:
    :return:
    """
    repo = RuleRepository(db)
    rule = await repo.update(id, data)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule

@router.delete("/{id}")
async def delete_rule(
        id: str,
        db=Depends(get_mongo_service),
        customer_id: str = Depends(validate_customer_exists)
):
    """
    :param id:
    :param db:
    :return:
    """
    repo = RuleRepository(db)
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"status": "deleted"}

@router.post("/~")
async def batch_process_rules(
    customer_id: str = Depends(validate_customer_exists),
    actions: List[RuleBatchItem] = [],
    db=Depends(get_mongo_service),
)->JSONResponse:
    """

    :param customer_id:
    :param actions:
    :param db:
    :return: JSONResponse
    """
    results = []
    repo = RuleRepository(db)

    for action in actions:
        try:
            if action.operation == "create":
                data = action.data.dict()
                data["customer_id"] = customer_id
                result = await repo.create(data)
            elif action.operation == "update":
                result = await repo.update(action.data.id, action.data)
            elif action.operation == "delete":
                result = await repo.delete(action.data.id)
            else:
                result = {"error": "Unsupported operation"}

            # Append to results list successful operation or operation which fails without raising any exception
            if result is not None and result is not False:
                result = {"success": f"{action.operation} successfully finished with data: {action.data.model_dump(exclude_unset=True)}", "operation": action.operation}
            else:
                result ={"error": f"{action.operation} unexpectedly failed", "operation": action.operation}
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "operation": action.operation})
    return JSONResponse(content=results)