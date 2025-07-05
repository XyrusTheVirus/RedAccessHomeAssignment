from functools import wraps
from typing import Callable, Optional, Any

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from services.audit_emitter import AuditLogger


def audit_action(operation: str):
    """
     Decorator to automatically log rule_audit_logs after create/update/delete operations.
     Extracts rule_id, customer_id, and body from args or kwargs.
     """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)

            body: Optional[dict] = None

            def to_object_id(value: Any) -> Optional[ObjectId]:
                try:
                    return ObjectId(str(value)) if value else None
                except (InvalidId, TypeError):
                    return None

            # Try extracting from kwargs first
            rule_id = to_object_id(kwargs.get("rule_id"))
            customer_id = to_object_id(kwargs.get("customer_id"))

            # Scan args for Pydantic models or other data
            for arg in args:
                if isinstance(arg, BaseModel):
                    body = arg.model_dump()
                    customer_id = customer_id or to_object_id(getattr(arg, "customer_id", None))
                    rule_id = rule_id or to_object_id(getattr(arg, "id", None))
                elif isinstance(arg, dict):
                    body = body or arg
                    customer_id = customer_id or to_object_id(arg.get("customer_id"))
                    rule_id = rule_id or to_object_id(arg.get("id"))
                elif isinstance(arg, str) and ObjectId.is_valid(arg):
                    oid = ObjectId(arg)
                    if not customer_id:
                        customer_id = oid
                    elif not rule_id:
                        rule_id = oid

            # Emit audit log if at least customer_id is known
            if customer_id:
                await self.audit.log(
                    rule_id=rule_id,
                    customer_id=customer_id,
                    operation=operation,
                    body=body,
                )

            return result

        return wrapper

    return decorator
