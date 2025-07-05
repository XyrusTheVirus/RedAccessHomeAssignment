from datetime import datetime
from typing import Optional

from bson import ObjectId
from events.rule_event import emit_rule_audit


class AuditLogger:
    def __init__(self, user: str = "system"):
        self.user = user

    async def log(
            self,
            *,
            rule_id: ObjectId,
            customer_id: ObjectId,
            operation: str,
            body: Optional[dict] = None,
    ):
        """
        Logs every rule operation application (create, delete, update)

        :param body:
        :param rule_id:
        :param customer_id:
        :param operation:
        """
        await emit_rule_audit({
            "rule_id": rule_id,
            "customer_id": customer_id,
            "operation": operation,
            "user": self.user,
            "timestamp": datetime.now(),
            "body": body,
        })
