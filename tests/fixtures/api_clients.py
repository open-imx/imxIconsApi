import pytest

from fastapi.testclient import TestClient
from fastapi import FastAPI

from imxIconApi.routers.v1 import get_icons, get_url
from imxIconApi.api import app
from imxIconApi.routers import icon_lib_page


@pytest.fixture(scope="module")
def fast_api_limiter_client():
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        return {"message": "Success"}


    @app.get("/")
    async def test_root_endpoint():
        return {"message": "Success"}

    return TestClient(app)


@pytest.fixture(scope="module")
def fast_api_api_client():
    return TestClient(app)


@pytest.fixture(scope="module")
def fast_api_library_client():
    return TestClient(icon_lib_page.router)


@pytest.fixture(scope="module")
def fast_api_icon_client():
    app = FastAPI()
    app.include_router(get_icons.router)
    client = TestClient(app)
    return client

@pytest.fixture(scope="module")
def fast_api_icon_url_client():
    app = FastAPI()
    app.include_router(get_url.router)
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def openapi_spec(fast_api_icon_client):
    response = fast_api_icon_client.get("/openapi.json")
    assert response.status_code == 200
    return response.json()
