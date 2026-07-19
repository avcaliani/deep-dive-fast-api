from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app import dependencies
from app.models import Mood

router = APIRouter(prefix="/mood", tags=["mood"], dependencies=[Depends(dependencies.get_user)])


@router.get("/{item}")
async def mood(
    item: Mood, text_mode: Optional[str] = Query(None, min_length=4, max_length=8, regex=r"CAPS(LOCK)?")
):
    messages = {
        Mood.happy: "If in doubt, Meriadoc, always follow your nose!",
        Mood.angry: "You must trust yourself. Trust your own strength.",
        Mood.insightful: "Even the very wise cannot see all ends.",
    }
    msg = messages.get(item)
    return {
        "message": msg.upper() if text_mode in ["CAPS", "CAPSLOCK"] else msg,
        "item": item,
        "consulted_at": datetime.utcnow(),
    }
