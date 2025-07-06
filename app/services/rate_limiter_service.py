import json
import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from databases.mongo import MongoService
from databases.redis import RedisService
from redis.exceptions import LockError


class RateLimiterService:
    def __init__(
            self,
            redis: RedisService,
            mongo: MongoService
    ):
        self.collection = mongo.get_db().get_collection("customers")
        self.redis = redis.get_client()

    async def is_allowed(self, customer_id: str) -> tuple[bool, Optional[str], Optional[int]]:
        """
        Validates whether the number of requests per customer haven't reached the limit
        :param customer_id:
        :return: tuple[bool, Optional[str], Optional[int]]
        """
        try:
            customer_oid = ObjectId(customer_id)
        except InvalidId:
            return False, "Invalid customer_id", 400

        redis_key = f"rate_limit:{customer_id}"
        lock_key = f"lock:{customer_id}"
        now = datetime.now()

        lock = self.redis.lock(lock_key, timeout=3, blocking_timeout=2)

        try:
            async with lock:
                # Read or fallback
                data = await self.redis.get(redis_key)
                if data:
                    customer_data = json.loads(data)
                else:
                    customer = await self.collection.find_one({"_id": customer_oid})
                    if not customer:
                        return False, "Customer not found", 404

                    customer_data = {
                        "request_rate_limit": customer["request_rate_limit"],
                        "last_request": now.isoformat(),
                        "current_number_of_requests": 0
                    }

                # Time check
                last_request = datetime.fromisoformat(customer_data["last_request"])
                seconds_since_last = (now - last_request).total_seconds()

                if seconds_since_last > 60:
                    customer_data["current_number_of_requests"] = 1
                else:
                    if customer_data["current_number_of_requests"] >= customer_data["request_rate_limit"]:
                        return False, "Too Many Requests", 429
                    customer_data["current_number_of_requests"] += 1

                customer_data["last_request"] = now.isoformat()
                await self.redis.set(redis_key, json.dumps(customer_data), ex=120)

        except LockError:
            logging.warning(f"Could not acquire Redis lock for customer {customer_id}")
            return False, "Rate limiter temporarily unavailable", 503

        return True, None, None
