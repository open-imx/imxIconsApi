import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

request_counter: int = 0
last_request_time: float = time.time()
rate_limit_window: int = 60
max_requests_per_window: int = 10


class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global last_request_time, request_counter

        no_limit = False

        # check if header has sponsor key
        api_key = [
            _[0]
            for _ in request.headers.raw
            if _[0] == b"x-api-key" and _[1] == b"TODO"
        ]
        if len(api_key) != 0:
            no_limit = True

        # check if no limit page
        url_to_check = f"{request.url}".replace(f"{request.base_url}", "")
        if url_to_check == "":
            no_limit = True
        elif "doc" in url_to_check or "docs" in url_to_check:
            no_limit = True

        if no_limit:
            return await call_next(request)

        # Reset the counter if the rate limit window has passed
        current_time = time.time()
        if current_time - last_request_time > rate_limit_window:
            request_counter = 0
            last_request_time = current_time

        # Count
        request_counter += 1

        # Check if the request limit has been exceeded
        if request_counter > max_requests_per_window:
            return JSONResponse(
                {
                    "error": f"Global app rate limit exceeded: {max_requests_per_window}/{rate_limit_window} sec",
                    "msg": "get sponsor key",
                },
                status_code=429,
            )

        # Otherwise, process the request
        response = await call_next(request)
        return response
