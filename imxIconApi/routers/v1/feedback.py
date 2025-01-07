import re

import httpx
from fastapi import APIRouter, HTTPException, Request, status, Depends
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

WHITELIST_DOMAINS = ["https://open-imx.github.io"]
DISCORD_WEBHOOK_URL = ""

router = APIRouter(tags=["feedback"])
limiter = Limiter(key_func=get_remote_address)


class Feedback(BaseModel):
    icon_name: str
    icon_url: str
    feedback_text: str


async def enforce_domain_whitelist(request: Request):
    origin = request.headers.get("origin")
    if origin and origin not in WHITELIST_DOMAINS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Origin not allowed",
        )

async def send_to_discord(feedback: Feedback):
    payload = {
        "content": f"**Feedback on {feedback.icon_name} Received!**\n\n"
                   f"**Icon page:** {feedback.icon_url}\n\n"
                   f"{'---'*5}\n"
                   f"{feedback.feedback_text}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Raise an error if the request fails


def validate_feedback(feedback: Feedback) -> bool:
    if len(feedback.text) < 10 or feedback.text.strip().lower() == "string":
        return False

    if any(re.search(r'http[s]?://', str(value)) for value in
           [feedback.text, feedback.subject, feedback.username, feedback.email]):
        return False

    if any(re.search(r'[^\w\s]', str(value)) for value in
           [feedback.text, feedback.subject, feedback.username, feedback.email]):
        return False

    return True


@router.post(
    "/feedback",
    dependencies=[Depends(enforce_domain_whitelist)],
    include_in_schema=False
)
@limiter.limit("1/minute")
async def submit_feedback(request: Request, feedback: Feedback):
    try:
        if not validate_feedback(feedback):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or suspicious feedback content. Please ensure your feedback is original and meaningful."
            )

        await send_to_discord(feedback)
        return {"message": "Feedback submitted successfully"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send feedback to Discord: {str(e)}"
        )
