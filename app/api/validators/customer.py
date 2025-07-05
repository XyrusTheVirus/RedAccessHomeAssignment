from bson import ObjectId
from databases.mongo import MongoService
from dependencies import get_mongo_service
from fastapi import Depends, HTTPException, Path


async def validate_customer_exists(
        customer_id: str = Path(...),
        mongo: MongoService = Depends(get_mongo_service)
) -> str:
    """
    Checks whether the customer ID (Mongo ObjectId) coming from the http request exists, else throwing exception

    :param customer_id:
    :param mongo:
    :return:
    """
    db = mongo.get_db()
    try:
        customer_obj_id = ObjectId(customer_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid customer ObjectId")
    customer = await db.customers.find_one({"_id": customer_obj_id})

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return str(customer["_id"])
