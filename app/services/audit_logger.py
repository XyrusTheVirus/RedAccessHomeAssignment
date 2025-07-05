import logging

from events.rule_event import on_rule_audit
from dependencies import get_mongo_service

@on_rule_audit
async def log_rule_audit(payload):
    """
    Writes rule operation to audit log
    :param payload:
    """
    collection = get_mongo_service().get_db().get_collection("rule_audit_logs")
    await collection.insert_one({
        "rule_id": payload["rule_id"],
        "customer_id": payload["customer_id"],
        "operation": payload["operation"],
        "user": payload["user"],
        "timestamp": payload["timestamp"],
        "body": payload["body"],
    })