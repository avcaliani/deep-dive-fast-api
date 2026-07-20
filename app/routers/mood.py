from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app import dependencies
from app.models import Mood

# Duff Rewards Club: daily "how's Duff treating you?" check-in.
router = APIRouter(prefix="/mood", tags=["mood"], dependencies=[Depends(dependencies.get_user)])


@router.get("/{item}")
async def mood(
    item: Mood, text_mode: Optional[str] = Query(None, min_length=4, max_length=8, pattern=r"CAPS(LOCK)?")
):
    messages = {
        Mood.happy: "Woohoo!",
        Mood.angry: "Why you little--!",
        Mood.insightful: "Kids, you tried your best and you failed miserably. The lesson is, never try.",
    }
    msg = messages.get(item)
    return {
        "message": msg.upper() if text_mode in ["CAPS", "CAPSLOCK"] else msg,
        "item": item,
        "consulted_at": datetime.now(timezone.utc),
    }
