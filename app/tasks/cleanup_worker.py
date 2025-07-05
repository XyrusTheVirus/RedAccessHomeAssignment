from datetime import date, datetime, time
from celery_worker import celery_app
from dependencies import get_mongo_service

@celery_app.task
def delete_expired_rules():
    db = get_mongo_service()  # simulate Depends()
    collection = db.get_db().get_collection("rules")
    today = datetime.combine(date.today(), time.min)

    result = collection.delete_many({
        "expired_date": {"$lt": today}
    })

    print(f"[cleanup] Deleted {result.deleted_count} expired rules")