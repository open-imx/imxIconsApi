import re
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from fastapi.responses import FileResponse
from imxIcons.domain.icon_library import ICON_DICT
from imxIcons.domain.supportedImxVersions import ImxVersionEnum
from imxIcons.iconService import IconService
from imxIcons.iconServiceModels import IconModel, IconRequestModel

from imxIconApi.exceptions import ErrorCode, ErrorModel

router = APIRouter(tags=["icons"])

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

    for icon_dict in ICON_DICT.values():
        if imx_version.name in icon_dict:
            result.extend(
                IconModel(**item.__dict__) for item in icon_dict[imx_version.name]
            )

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
async def get_svg_icon_as_file(
    item: IconRequestModel, imx_version: ImxVersionEnum, qgis_supported: bool = False
):
    svg_content = IconService.get_svg(item, imx_version)
    match = re.search(r'<svg[^>]*\bname="([^"]*)"', svg_content)

    if match:
        svg_name = match.group(1)
    else:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SVG name attribute not found",
        )

    headers = {"Content-Disposition": f"attachment; filename={svg_name}.svg"}

    return Response(content=svg_content, media_type="image/svg+xml", headers=headers)


@router.post(
    path="/{imx_version}/svg/url",
    tags=["url"],
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
async def get_svg_icon_as_url(
    item: IconRequestModel,
    imx_version: ImxVersionEnum,
    request: Request,
    qgis_supported: bool = False,
):
    svg_content = IconService.get_svg(item, imx_version)
    match = re.search(r'<svg[^>]*\bname="([^"]*)"', svg_content)

    if match:
        svg_name = match.group(1)
    else:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SVG name attribute not found",
        )

    return f"{request.base_url}{imx_version.value}/svg/{svg_name}.svg"


@router.get(
    path="/{imx_version}/svg/{icon_name}.svg",
    tags=["url"],
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
