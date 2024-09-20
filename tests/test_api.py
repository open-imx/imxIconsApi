import pytest
from unittest.mock import patch


def test_app_startup(mocker, fast_api_api_client):
    with patch("imxIconApi.api.templates.get_template") as mock_get_template:
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "<html><body>Landing Page</body></html>"

        response = fast_api_api_client.get("/")
        assert response.status_code == 200
        assert "Landing Page" in response.text
