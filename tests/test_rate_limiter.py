import pytest
import time

from unittest.mock import patch

from imxIconApi.rateLimiter import RATE_LIMIT_WINDOW, MAX_REQUESTS_PER_WINDOW


def test_basic_request(fast_api_limiter_client):
    response = fast_api_limiter_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}


def test_rate_limit_exceeded(fast_api_limiter_client):
    # Patch the global variables directly
    with patch('imxIconApi.rateLimiter.LAST_REQUEST_TIME', time.time() - RATE_LIMIT_WINDOW - 1):
        with patch('imxIconApi.rateLimiter.REQUEST_COUNTER', MAX_REQUESTS_PER_WINDOW):
            for _ in range(MAX_REQUESTS_PER_WINDOW):
                response = fast_api_limiter_client.get("/test")
                assert response.status_code == 200

            # After exceeding the limit
            response = fast_api_limiter_client.get("/test")
            assert response.status_code == 429
            assert response.json() == {
                "error": f"Global app rate limit exceeded: {MAX_REQUESTS_PER_WINDOW}/{RATE_LIMIT_WINDOW} sec",
                "msg": "get sponsor key",
            }


def test_no_limit_url(fast_api_limiter_client):
    response = fast_api_limiter_client.get("/docs")
    assert response.status_code == 200


def test_no_limit_root(fast_api_limiter_client):
    response = fast_api_limiter_client.get("/")
    assert response.status_code == 200


def test_no_limit_header(fast_api_limiter_client):
    headers = {"X-API-Key": "TODO"}
    for item in [fast_api_limiter_client.get("/test", headers=headers) for i in range(0, 20)]:
        assert item.status_code == 200
