from os import getenv

from databases.mongo import MongoService
from databases.redis import RedisService

mongo_service = MongoService()


def get_mongo_service() -> MongoService:
    return mongo_service


redis_service = RedisService(
    getenv("REDIS_HOST", "redis"),
    int(getenv("REDIS_PORT", 6379)),
    int(getenv("REDIS_DB", 0))
)


def get_redis_service() -> RedisService:
    return redis_service
