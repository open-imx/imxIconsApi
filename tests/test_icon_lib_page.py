import pytest


def test_render_icons(mocker, fast_api_library_client):
    mock_get_template = mocker.patch("imxIconApi.routers.icon_lib_page.templates.get_template")
    mock_template = mock_get_template.return_value
    mock_template.render.return_value = "<html><body>Icons Page</body></html>"

    mock_get_svg = mocker.patch("imxIconApi.routers.icon_lib_page.IconService.get_svg")
    mock_get_svg.return_value = "<svg>Mock SVG</svg>"

    response = fast_api_library_client.get("/IMX-v1.2.4/icons")
    assert response.status_code == 200
    assert "Icons Page" in response.text

    response = fast_api_library_client.get("/IMX-v5.0.0/icons")
    assert response.status_code == 200
    assert "Icons Page" in response.text

