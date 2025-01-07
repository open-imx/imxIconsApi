from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from imxIcons import __version__ as imx_icon_version
from imxIcons.domain.supportedImxVersions import ImxVersionEnum

from imxIconApi import __version__ as api_version
from imxIconApi.api_description import description

# from imxIconApi.rateLimiter import RateLimiterMiddleware
from imxIconApi.routers import icon_lib_page
from imxIconApi.routers.v1 import get_icons, get_url, feedback
from imxIconApi.startup import create_asset_folder

# https://github.com/Intility/fastapi-azure-auth


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    await create_asset_folder()
    yield


app = FastAPI(
    title="OpenImx.Icons",
    version=f"📡{api_version} | ⚙️{imx_icon_version}",
    description=description,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(RateLimiterMiddleware)

app.include_router(icon_lib_page.router)
app.include_router(get_icons.router)
app.include_router(get_url.router)
app.include_router(feedback.router)

templates = Jinja2Templates(directory="imxIconApi/templates")

IMX_VERSIONS = [version.value for version in ImxVersionEnum]


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing_page(request: Request):
    _ = templates.get_template("landing_page.html")
    return HTMLResponse(content=_.render(imx_versions=IMX_VERSIONS), status_code=200)
