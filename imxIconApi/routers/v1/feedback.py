# import os
# import re
# from itertools import chain
#
# import httpx
# from dotenv import load_dotenv
# from fastapi import APIRouter, Depends, HTTPException, Request, status
# from imxIcons.domain.supportedImxVersions import ImxVersionEnum
# from imxIcons.iconService import IconService
# from pydantic import BaseModel
# from slowapi import Limiter
# from slowapi.util import get_remote_address
#
# load_dotenv()
#
#
# WHITELIST_DOMAINS = os.getenv("WHITELIST_DOMAINS", "")
# DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
#
#
# router = APIRouter(tags=["feedback"])
# limiter = Limiter(key_func=get_remote_address)
#
#
# ICON_NAMES = set(
#     chain.from_iterable(
#         IconService.get_all_icons(version).keys()
#         for version in [
#             imx_version for imx_version in ImxVersionEnum if imx_version.value
#         ]
#     )
# )
#
#
# class Feedback(BaseModel):
#     icon_name: str
#     icon_url: str
#     imx_version: str
#     feedback_text: str
#
#
# async def enforce_domain_whitelist(request: Request):
#     origin = request.headers.get("origin")
#     if origin and origin not in WHITELIST_DOMAINS:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Origin not allowed",
#         )
#
#
# async def send_to_discord(feedback: Feedback):
#     payload = {
#         "content": f"**Feedback on Icon {feedback.icon_name} Received!**\n"
#         f"Imx version: {feedback.imx_version}\n"
#         f"Icon page: {feedback.icon_url}\n"
#         f"\n"
#         f"***{feedback.feedback_text}***\n"
#         f"\n{'--' * 10}\n"
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post(DISCORD_WEBHOOK_URL, json=payload)
#         response.raise_for_status()
#
#
# def validate_feedback(feedback: Feedback) -> bool:
#     request_model_fields = [
#         feedback.icon_name,
#         feedback.icon_url,
#         feedback.feedback_text,
#     ]
#
#     # Reject Request body whit 'string' values (like in the docs)
#     for item in request_model_fields:
#         if item.strip().lower() == "string":
#             return False
#
#     # check if icon name is in service
#     if feedback.icon_name not in ICON_NAMES:
#         return False
#
#     if feedback.imx_version not in list(ImxVersionEnum.__members__):
#         return False
#
#     # check if icon url haz valid root
#     if "https://open-imx.github.io/imxIcons/generated/" not in feedback.icon_url:
#         return False
#
#     # Reject feedback that contains URLs in any of the fields
#     if any(
#         re.search(r"http[s]?://", str(value))
#         for value in [feedback.icon_name, feedback.feedback_text]
#     ):
#         return False
#
#     return True
#
#
# @router.post(
#     "/feedback",
#     dependencies=[Depends(enforce_domain_whitelist)],
#     # include_in_schema=False
# )
# @limiter.limit("1/minute")
# async def submit_feedback(request: Request, feedback: Feedback):
#     try:
#         if not validate_feedback(feedback):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid or suspicious feedback content. Please ensure your feedback is original and meaningful.",
#             )
#
#         await send_to_discord(feedback)
#         return {"message": "Feedback submitted successfully"}  # NOQA TRY300
#     except httpx.HTTPStatusError as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to send feedback to Discord: {str(e)}",
#         )
