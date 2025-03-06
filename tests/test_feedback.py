import pytest
from imxIconApi.routers.v1.feedback import router
from imxIconApi.routers.v1.feedback import validate_feedback, Feedback, enforce_domain_whitelist
from imxIcons.domain.supportedImxVersions import ImxVersionEnum
from imxIcons.iconService import IconService
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_icon_service():
    with patch.object(IconService, 'get_all_icons', return_value={"valid_icon": {}}):
        yield


@pytest.fixture
def valid_feedback():
    return Feedback(
        icon_name="SignalLow",
        icon_url="https://open-imx.github.io/imxIcons/generated/SignalLow.svg",
        imx_version=ImxVersionEnum.v124.name,
        feedback_text="Great icon!"
    )


def test_valid_feedback(valid_feedback, mock_icon_service):
    assert validate_feedback(valid_feedback) is True


def test_default_feedback(valid_feedback, mock_icon_service):
    invalid_feedback = valid_feedback.copy(update={"feedback_text": "string"})
    assert validate_feedback(invalid_feedback) is False


def test_invalid_icon_name_feedback(valid_feedback, mock_icon_service):
    invalid_feedback = valid_feedback.copy(update={"icon_name": "InvalidIcon"})
    assert validate_feedback(invalid_feedback) is False


def test_invalid_imx_version_feedback(valid_feedback, mock_icon_service):
    invalid_feedback = valid_feedback.copy(update={"imx_version": "v0"})
    assert validate_feedback(invalid_feedback) is False


def test_invalid_origin_feedback(valid_feedback, mock_icon_service):
    invalid_feedback = valid_feedback.copy(update={"icon_url": "https://xxxx-imx.github.io/imxIcons/generated/SignalLow.svg"})
    assert validate_feedback(invalid_feedback) is False


def test_url_feedback(valid_feedback, mock_icon_service):
    invalid_feedback = valid_feedback.copy(update={"feedback_text": "http:// Great icon!"})
    assert validate_feedback(invalid_feedback) is False

