from enum import Enum

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: str | dict[str, str]


class ErrorCodeReasonModel(BaseModel):
    code: str
    reason: str


class ErrorCode(str, Enum):
    IMX_PATH_NOT_FOUND = "IMX PATH NOT FOUND"


class IconApiException(Exception):
    pass
