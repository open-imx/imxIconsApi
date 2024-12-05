import os

import pytest
from fastapi import status


@pytest.mark.parametrize(
    "imx_version, icon_name, expected_status_code",
    [
        ("IMX-v1.2.4", "AutomaticPermissiveGantryArrow", status.HTTP_200_OK),
        ("IMX-v1.2.4", "non_existing_icon", status.HTTP_404_NOT_FOUND),
        ("xxxxx", "icon1", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ]
)
@pytest.mark.skipif(
    os.getenv('CI') == 'true', reason="Skipping icon generation tests in CI environment"
)
def test_get_svg_url(imx_version, icon_name, expected_status_code, fast_api_icon_client):
    response = fast_api_icon_client.get(f"/{imx_version}/svg/{icon_name}.svg")
    assert response.status_code == expected_status_code

    if expected_status_code == status.HTTP_200_OK:
        assert response.headers["content-type"] == "image/svg+xml;charset=utf-8"


@pytest.mark.parametrize(
    "imx_version, request_data, expected_status_code, icon_url",
    [
        ("IMX-v1.2.4", {"imx_path": "Signal", "properties": {"signalType": "AutomaticPermissive","signalPosition": "High","isMountedOnGantry": "True"}} , 200, 'http://testserver/IMX-v1.2.4/svg/AutomaticPermissiveGantry.svg'),
    ]
)
@pytest.mark.skipif(
    os.getenv('CI') == 'true', reason="Skipping icon generation tests in CI environment"
)
def test_post_svg_url(imx_version, request_data, expected_status_code, icon_url, fast_api_icon_client):
    response = fast_api_icon_client.post(f"/{imx_version}/svg/url/", json=request_data)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.text == icon_url
