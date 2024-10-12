import base64

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from imxIcons.domain import ICON_DICT
from imxIcons.domain.supportedImxVersions import ImxVersionEnum
from imxIcons.iconService import IconService
from imxIcons.iconServiceModels import IconRequestModel

router = APIRouter()

templates = Jinja2Templates(directory="imxIconApi/templates")

IMX_VERSIONS = [version.value for version in ImxVersionEnum]


async def get_svg_content(
    svg_request: IconRequestModel, imx_version: ImxVersionEnum
) -> str:
    return IconService.get_svg(svg_request, imx_version)


@router.get(
    "/{imx_version}/icons", response_class=HTMLResponse, include_in_schema=False
)
async def render_icons(request: Request, imx_version: ImxVersionEnum):
    data: dict = {}
    for imx_path, icon_entities in ICON_DICT.items():
        data[imx_path] = {}
        for icon_entity in icon_entities[imx_version.name]:
            svg_content = await get_svg_content(
                IconRequestModel(imx_path=imx_path, properties=icon_entity.properties),
                imx_version,
            )
            encoded_svg = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
            data[imx_path][icon_entity.icon_name] = {
                "properties": icon_entity.properties,
                "svg": encoded_svg,
            }
    return templates.TemplateResponse(
        "icons.html", {"request": request, "data": data, "imx_version": imx_version}
    )
