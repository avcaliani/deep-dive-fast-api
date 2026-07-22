from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query

from app import dependencies
from app.config import settings
from app.models import Mood
from app.services import user as service

# Dunder Mifflin: daily morale check-in, pays out in Schrute Bucks.
CHECKIN_POINTS = settings.CHECKIN_POINTS
router = APIRouter(prefix="/mood", tags=["mood"], dependencies=[Depends(dependencies.get_user)])


@router.get("/{item}")
async def mood(
    item: Mood,
    text_mode: str | None = Query(None, min_length=4, max_length=8, pattern=r"CAPS(LOCK)?"),
    user: dict = Depends(dependencies.get_user),
):
    messages = {
        Mood.happy: "That's what she said!",
        Mood.angry: "FALSE.",
        Mood.insightful: "Sometimes I'll start a sentence and I don't even know where "
        "it's going. I just hope I find it along the way.",
    }
    msg = messages.get(item)
    updated_user = await service.add_points(user["email"], CHECKIN_POINTS)
    return {
        "message": msg.upper() if text_mode in ["CAPS", "CAPSLOCK"] else msg,
        "item": item,
        "schrute_bucks_earned": CHECKIN_POINTS,
        "balance": updated_user["points"],
        "consulted_at": datetime.now(timezone.utc),
    }
