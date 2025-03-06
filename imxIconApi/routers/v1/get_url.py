import re
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import FileResponse
from imxIcons.domain.supportedIconTypes import IconTypesEnum
from imxIcons.domain.supportedImxVersions import ImxVersionEnum
from imxIcons.iconService import IconService
from imxIcons.iconServiceModels import IconRequestModel

from imxIconApi.exceptions import ErrorCode, ErrorModel

router = APIRouter(tags=["icons"])

IMX_VERSIONS = [version.value for version in ImxVersionEnum]


@router.post(
    path="/{imx_version}/svg/url",
    response_class=Response,
    response_description="SVG file",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.IMX_PATH_NOT_FOUND: {
                            "summary": "IMX path is not found / not supported by the icon service.",
                            "value": {"detail": ErrorCode.IMX_PATH_NOT_FOUND},
                        },
                        "SVG_NAME_NOT_FOUND": {
                            "summary": "SVG name attribute not found.",
                            "value": {"detail": "SVG name attribute not found"},
                        },
                    }
                }
            },
        },
    },
)
async def get_icon_url(
    item: IconRequestModel,
    imx_version: ImxVersionEnum,
    request: Request,
    icon_type: IconTypesEnum = IconTypesEnum.svg,
):
    # we do not check the asset folder, sometimes we do not have the assets
    svg_content = IconService.get_svg(item, imx_version, icon_type=icon_type)
    match = re.search(r'<svg[^>]*\bname="([^"]*)"', svg_content)

    if match:
        svg_name = match.group(1)
    else:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SVG name attribute not found",
        )

    suffix = ""
    if icon_type == IconTypesEnum.svg_dark:
        suffix = "-dark"
    elif icon_type == IconTypesEnum.qgis:
        suffix = "-qgis"
    elif icon_type == IconTypesEnum.qgis_dark:
        suffix = "-qgis-dark"

    return f"{request.base_url}{imx_version.value}/svg/{svg_name}{suffix}.svg"


@router.get(
    path="/{imx_version}/svg/{icon_name}.svg",
    response_description="SVG file",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "ErrorCode.IMX_PATH_NOT_FOUND": {
                            "summary": "IMX path is not found / not supported by the icon service.",
                            "value": {"detail": "IMX path is not found"},
                        },
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "File not found": {
                            "summary": "The requested file was not found",
                            "value": {"detail": "File not found"},
                        },
                    }
                }
            },
        },
    },
)
async def get_svg_url(
    imx_version: ImxVersionEnum,
    icon_name: str,
):
    if not imx_version:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST, detail="IMX path not found"
        )

    static_base_path = Path(__file__).parent.parent.parent / "static" / imx_version.name
    svg_file_path = static_base_path / f"{icon_name}.svg"

    if not svg_file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(svg_file_path, media_type="image/svg+xml;charset=utf-8")
