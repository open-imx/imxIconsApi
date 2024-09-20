import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


REQUEST_COUNTER: int = 0
LAST_REQUEST_TIME: float = time.time()
RATE_LIMIT_WINDOW: int = 60
MAX_REQUESTS_PER_WINDOW: int = 10


class RateLimiterMiddleware(BaseHTTPMiddleware):

    @staticmethod
    def _has_api_key(request: Request) -> bool:
        api_key = [
            _[0]
            for _ in request.headers.raw
            if _[0] == b"x-api-key" and _[1] == b"TODO"
        ]
        if len(api_key) != 0:
            return True
        return False

    @staticmethod
    def _is_limited_page(request: Request) -> bool:
        url_to_check = f"{request.url}".replace(f"{request.base_url}", "")
        if url_to_check == "":
            return  True
        elif "doc" in url_to_check or "docs" in url_to_check:
            return True
        return False


    async def dispatch(self, request: Request, call_next):
        global LAST_REQUEST_TIME, REQUEST_COUNTER

        no_limit = False
        no_limit = True if self._has_api_key(request) else no_limit
        no_limit = True if self._is_limited_page(request) else no_limit
        if no_limit:
            return await call_next(request)

        # Reset the counter if the rate limit window has passed
        current_time = time.time()
        if current_time - LAST_REQUEST_TIME > RATE_LIMIT_WINDOW:
            REQUEST_COUNTER = 0
            LAST_REQUEST_TIME = current_time

        # Count
        REQUEST_COUNTER += 1

        # Check if the request limit has been exceeded
        if REQUEST_COUNTER > MAX_REQUESTS_PER_WINDOW:
            return JSONResponse(
                {
                    "error": f"Global app rate limit exceeded: {MAX_REQUESTS_PER_WINDOW}/{RATE_LIMIT_WINDOW} sec",
                    "msg": "get sponsor key",
                },
                status_code=429,
            )

        # Otherwise, process the request
        response = await call_next(request)
        return response
