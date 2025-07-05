import re

from fastapi import Request
from fastapi.responses import JSONResponse
from services.rate_limiter_service import RateLimiterService
from starlette.middleware.base import BaseHTTPMiddleware

CUSTOMER_ID_REGEX = re.compile(r"^/customers/(?P<customer_id>[a-f0-9]{24})/")


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limiter_service: RateLimiterService):
        super().__init__(app)
        self.rate_limiter = rate_limiter_service

    async def dispatch(self, request: Request, call_next):
        """
        Checks whether customer throttling configuration has reach the bar

        :param request:
        :param call_next:
        :return:
        """
        match = CUSTOMER_ID_REGEX.match(request.url.path)
        if not match:
            # Path does not match pattern, skip rate limiting
            return await call_next(request)

        customer_id = match.group("customer_id")
        if not customer_id:
            return JSONResponse(status_code=400, content={"detail": "Missing customer_id in path"})

        allowed, error, status = await self.rate_limiter.is_allowed(customer_id)
        if not allowed:
            return JSONResponse(status_code=status or 400, content={"detail": error})

        return await call_next(request)
