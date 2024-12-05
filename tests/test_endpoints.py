import os

import pytest
from fastapi import status


def test_openapi_endpoints(openapi_spec):
    assert any(path == "/{imx_version}/paths" for path in openapi_spec["paths"].keys())
    assert any(path == "/{imx_version}/mapping" for path in openapi_spec["paths"].keys())
    assert any(path == "/{imx_version}/svg/str" for path in openapi_spec["paths"].keys())
    assert any(path == "/{imx_version}/svg/file" for path in openapi_spec["paths"].keys())


def test_endpoint_details(openapi_spec):

    def test_imx_version_parameter(_data):
        _data_ = [_ for _ in _data if _["name"] == "imx_version"]
        assert len(_data_) == 1
        assert _data_[0]["name"] == "imx_version"
        assert _data_[0]["in"] == "path"
        assert _data_[0]["required"] == True
        assert _data_[0]["schema"]["$ref"] == '#/components/schemas/ImxVersionEnum'

    def test_imx_path_parameter(_data):
        _data_ = [_ for _ in _data if _["name"] == "imx_path"]
        assert len(_data_) == 1
        assert _data_[0]["name"] == "imx_path"
        assert _data_[0]["in"] == "query"
        assert _data_[0]["required"] == False
        assert _data_[0]["schema"]["anyOf"] == [{'type': 'string'}, {'type': 'null'}]

    def test_qgs_parameter(_data):
        _data_ = [_ for _ in _data if _["name"] == "qgis_supported"]
        assert len(_data_) == 1
        assert _data_[0]["name"] == "qgis_supported"
        assert _data_[0]["in"] == "query"
        assert _data_[0]["required"] == False
        assert _data_[0]["schema"] == {'default': False, 'title': 'Qgis Supported', 'type': 'boolean'}

    def test_icon_request_body(_data):
        assert 'requestBody' in _data.keys()
        assert _data["requestBody"]['required'] == True
        assert _data["requestBody"]['content']['application/json']['schema']['$ref'] == '#/components/schemas/IconRequestModel'

    paths = openapi_spec["paths"]

    # Check /{imx_version}/paths endpoint
    assert "/{imx_version}/paths" in paths
    assert "get" in paths["/{imx_version}/paths"]
    assert "200" in paths["/{imx_version}/paths"]["get"]["responses"]
    assert "parameters" in paths["/{imx_version}/paths"]["get"]
    assert len(paths["/{imx_version}/paths"]["get"]["parameters"]) == 1
    test_imx_version_parameter(paths["/{imx_version}/paths"]["get"]["parameters"])

    # Check /{imx_version}/mapping endpoint
    assert "/{imx_version}/mapping" in paths
    assert "get" in paths["/{imx_version}/mapping"]
    assert "200" in paths["/{imx_version}/mapping"]["get"]["responses"]
    assert "parameters" in paths["/{imx_version}/mapping"]["get"]
    assert len(paths["/{imx_version}/mapping"]["get"]["parameters"]) == 2
    test_imx_version_parameter(paths["/{imx_version}/mapping"]["get"]["parameters"])
    test_imx_path_parameter(paths["/{imx_version}/mapping"]["get"]["parameters"])

    # Check /{imx_version}/svg/str endpoint
    assert "/{imx_version}/svg/str" in paths
    assert "post" in paths["/{imx_version}/svg/str"]
    assert "200" in paths["/{imx_version}/svg/str"]["post"]["responses"]
    assert "parameters" in paths["/{imx_version}/svg/str"]["post"]
    assert len(paths["/{imx_version}/svg/str"]["post"]["parameters"]) == 2
    test_imx_version_parameter(paths["/{imx_version}/svg/str"]["post"]["parameters"])
    test_qgs_parameter(paths["/{imx_version}/svg/str"]["post"]["parameters"])
    test_icon_request_body(paths["/{imx_version}/svg/str"]["post"])

    # Check /{imx_version}/svg/file endpoint
    assert "/{imx_version}/svg/file" in paths
    assert "post" in paths["/{imx_version}/svg/file"]
    assert "200" in paths["/{imx_version}/svg/file"]["post"]["responses"]
    assert "parameters" in paths["/{imx_version}/svg/file"]["post"]
    assert len(paths["/{imx_version}/svg/file"]["post"]["parameters"]) == 2
    test_imx_version_parameter(paths["/{imx_version}/svg/file"]["post"]["parameters"])
    test_qgs_parameter(paths["/{imx_version}/svg/file"]["post"]["parameters"])
    test_icon_request_body(paths["/{imx_version}/svg/file"]["post"])


@pytest.mark.parametrize("imx_version, expected_status_code", [
    ("IMX-v1.2.4", 200),
    ("IMX-v5.0.0", 200),
    ("IMX-v1.2.5", 422),
])
def test_get_all_supported_imx_paths(imx_version: str, expected_status_code: int, fast_api_icon_client):
    response = fast_api_icon_client.get(f"/{imx_version}/paths")
    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        response_data = response.json()
        assert isinstance(response_data, list)
        assert all(isinstance(item, str) for item in response_data)
    elif expected_status_code == 422:
        assert "detail" in response.json()


@pytest.mark.parametrize("imx_version, imx_path, expected_status_code", [
    ("IMX-v1.2.4", "Signal", 200),
    ("IMX-v5.0.0", None, 200),
    ("IMX-v1.2.4", "Zignal", 400),
    ("IMX-v1.2.5", "Signal", 422),
])
def test_get_icon_mapping(imx_version: str, imx_path: str, expected_status_code: int, fast_api_icon_client):
    url = f"/{imx_version}/mapping"
    params = {"imx_path": imx_path} if imx_path is not None else {}
    response = fast_api_icon_client.get(url, params=params)
    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        response_data = response.json()
        assert isinstance(response_data, list)
    elif expected_status_code == 400:
        assert "detail" in response.json()


@pytest.mark.parametrize(
    "imx_version, request_data, expected_status_code",
    [
        ("IMX-v1.2.4", {"imx_path": "Signal", "properties": {"signalType": "AutomaticPermissive","signalPosition": "High","isMountedOnGantry": "True"}} , 200),
    ]
)
def test_get_svg_icon_as_string(imx_version, request_data, expected_status_code, fast_api_icon_client):
    response = fast_api_icon_client.post(f"/{imx_version}/svg/str", json=request_data)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.headers["Content-Type"] == "image/svg+xml"
        assert response.text.startswith("<svg")



@pytest.mark.parametrize(
    "imx_version, request_data, expected_status_code",
    [
        ("IMX-v1.2.4", {"imx_path": "Signal", "properties": {"signalType": "AutomaticPermissive","signalPosition": "High","isMountedOnGantry": "True"}} , 200),
    ]
)
def test_get_svg_icon_as_file(imx_version, request_data, expected_status_code, fast_api_icon_client):
    response = fast_api_icon_client.post(f"/{imx_version}/svg/file", json=request_data)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.headers["Content-Type"] == "image/svg+xml"
        assert response.text.startswith("<svg")

        matching_headers = [
            header_value
            for header in response.headers.raw
            for header_value in header
            if b'attachment; filename=' in header_value
        ]
        assert len(matching_headers) == 1
