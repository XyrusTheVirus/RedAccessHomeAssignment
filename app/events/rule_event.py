import asyncio
from datetime import datetime
from typing import Literal, TypedDict, Callable, Awaitable

from bson import ObjectId


class RuleAuditPayload(TypedDict):
    operation: Literal["create", "update", "delete"]
    rule_id: ObjectId
    customer_id: ObjectId
    user: str
    timestamp: datetime


_listeners: list[Callable[[RuleAuditPayload], Awaitable[None]]] = []


async def emit_rule_audit(payload: RuleAuditPayload):
    """

    :param payload:
    """
    for listener in _listeners:
        result = listener(payload)
        if asyncio.iscoroutine(result):
            await result
        else:
            result


def on_rule_audit(func: Callable[[RuleAuditPayload], Awaitable[None]]):
    """

    :param func:
    :return:
    """
    _listeners.append(func)
    return func
