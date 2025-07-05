import logging
import os

from fastapi import FastAPI

from api.middlewares.rate_limiter import RateLimiterMiddleware
from api.routes import api_router
from databases.mongo import MongoService
from databases.redis import RedisService
from dependencies import get_mongo_service
from dependencies import get_redis_service
from services.rate_limiter_service import RateLimiterService

logging.basicConfig(level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
app = FastAPI(redirect_slashes=False)

mongo: MongoService = get_mongo_service()
redis: RedisService = get_redis_service()

# Create service
rate_limiter_service = RateLimiterService(redis, mongo)
# Add middleware
app.add_middleware(
    RateLimiterMiddleware,
    rate_limiter_service=rate_limiter_service
)
app.include_router(api_router)


@app.on_event("shutdown")
async def shutdown():
    await redis.close()
    mongo.get_db().close()
