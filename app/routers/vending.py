from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app import dependencies
from app.config import settings
from app.models import VendingItem
from app.services import user as service

# Dunder Mifflin: office vending machine. Browsing is free, redeeming costs Schrute Bucks.
ITEMS = [VendingItem(**item) for item in settings.VENDING_ITEMS]

router = APIRouter(prefix="/vending", tags=["vending"], dependencies=[Depends(dependencies.get_user)])


def _get_item(item: int) -> VendingItem:
    if item < 0 or item >= len(ITEMS):
        raise HTTPException(status_code=404, detail=f"No vending item at index '{item}'!")
    return ITEMS[item]


@router.get("/")
async def catalog(limit: int | None = None):
    return {
        "items": ITEMS[:limit] if limit else ITEMS,
        "consulted_at": datetime.now(timezone.utc),
    }


@router.get("/{item}")
async def get_item(item: int):
    return {
        "item": item,
        "vending_item": _get_item(item),
        "consulted_at": datetime.now(timezone.utc),
    }


@router.post("/{item}")
async def redeem(item: int, user: dict = Depends(dependencies.get_user)):
    vending_item = _get_item(item)
    updated_user = await service.spend_points(user["email"], vending_item.cost)
    if updated_user is None:
        raise HTTPException(status_code=402, detail="Not enough Schrute Bucks!")
    return {
        "redeemed": vending_item,
        "balance": updated_user["points"],
        "redeemed_at": datetime.now(timezone.utc),
    }
