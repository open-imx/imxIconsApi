import re

from fastapi import APIRouter, HTTPException, Query, Response, status
from imxIcons.domain import ICON_DICT
from imxIcons.domain.supportedImxVersions import ImxVersionEnum
from imxIcons.iconService import IconService
from imxIcons.iconServiceModels import IconModel, IconRequestModel

from imxIconApi.exceptions import ErrorCode, ErrorModel

router = APIRouter()

IMX_VERSIONS = [version.value for version in ImxVersionEnum]


@router.get("/{imx_version}/paths")
async def get_all_supported_imx_paths(imx_version: ImxVersionEnum) -> list[str]:
    return [key for key, value in ICON_DICT.items() if imx_version.name in value]


@router.get(
    "/{imx_version}/mapping",
    response_model=list[IconModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.IMX_PATH_NOT_FOUND: {
                            "summary": "IMX path not found: not supported by the icon service.",
                            "value": {"detail": ErrorCode.IMX_PATH_NOT_FOUND},
                        },
                    }
                }
            },
        },
    },
)
async def get_icon_mapping(
    imx_version: ImxVersionEnum,
    imx_path: str | None = Query(None, description="Filter examples by imx_path"),
):
    result: list = []

    if imx_path:
        if imx_path not in ICON_DICT.keys():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.IMX_PATH_NOT_FOUND,
            )

        for values in ICON_DICT[imx_path].values():
            result.extend(
                IconModel(**item.__dict__)
                for item in values
                if item.imx_version == imx_version
            )
        return result

    for values in ICON_DICT.values():
        result.extend(IconModel(**item.__dict__) for item in values[imx_version.name])

    return result


@router.post(
    path="/{imx_version}/svg/str",
    response_class=Response,
    response_description="SVG string",
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
                    }
                }
            },
        },
    },
)
async def get_svg_icon_as_string(
    item: IconRequestModel, imx_version: ImxVersionEnum, qgis_supported: bool = False
):
    svg_content = IconService.get_svg(item, imx_version)
    return Response(content=svg_content, media_type="image/svg+xml")


@router.post(
    path="/{imx_version}/svg/file",
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
                    }
                }
            },
        },
    },
)
async def get_svg_icon_as_file(
    item: IconRequestModel, imx_version: ImxVersionEnum, qgis_supported: bool = False
):
    svg_content = IconService.get_svg(item, imx_version)
    svg_name = re.search(r'<svg[^>]*\bname="([^"]*)"', svg_content).group(1)

    headers = {"Content-Disposition": f"attachment; filename={svg_name}.svg"}

    return Response(content=svg_content, media_type="image/svg+xml", headers=headers)
