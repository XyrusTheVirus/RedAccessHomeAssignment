from databases.mongo import MongoService

mongo_service = MongoService()

def get_mongo_service() -> MongoService:
    return mongo_service