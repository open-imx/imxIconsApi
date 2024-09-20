import pytest
import time

from unittest.mock import patch

from imxIconApi.rateLimiter import rate_limit_window, max_requests_per_window


def test_basic_request(fast_api_limiter_client):
    response = fast_api_limiter_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}

def test_rate_limit_exceeded(fast_api_limiter_client):
    with patch('imxIconApi.rateLimiter.last_request_time', time.time() - rate_limit_window - 1):
        with patch('imxIconApi.rateLimiter.request_counter', max_requests_per_window):
            for _ in range(max_requests_per_window):
                response = fast_api_limiter_client.get("/test")
                assert response.status_code == 200

            response = fast_api_limiter_client.get("/test")
            assert response.status_code == 429
            assert response.json() == {
                "error": f"Global app rate limit exceeded: {max_requests_per_window}/{rate_limit_window} sec",
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
