from datetime import datetime
from random import choices, randint
from typing import Optional

from fastapi import APIRouter, Depends

from app import dependencies
from app.config import settings

SECRET = settings.SECRET
EMOJIS = settings.EMOJIS

router = APIRouter(prefix="/emoji", tags=["emoji"], dependencies=[Depends(dependencies.get_user)])


@router.get("/")
async def emojis(limit: Optional[int] = None):
    return {
        "lucky_emojis": choices(EMOJIS, k=limit if limit else randint(1, len(EMOJIS))),
        "secret": SECRET,
        "consulted_at": datetime.utcnow(),
    }


@router.get("/{item}")
async def get_emoji(item: int):
    return {"emoji": EMOJIS[item], "item": item, "item_type": type(item), "consulted_at": datetime.utcnow()}
