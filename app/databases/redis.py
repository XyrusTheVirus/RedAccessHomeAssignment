from redis.asyncio import Redis


class RedisService:
    def __init__(self, host: str = "redis" , port: int = 6379, db: int = 0):
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_client(self) -> Redis:
        return self.redis