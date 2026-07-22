from datetime import date, datetime, timezone
from enum import Enum
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field


class Mood(str, Enum):
    happy = "😁"
    angry = "😡"
    insightful = "🤔"


def _validate_object_id(value: Any) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ID!")
    return str(value)


PyObjectId = Annotated[str, BeforeValidator(_validate_object_id)]


class User(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    email: EmailStr
    birthdate: date
    mood: Mood | None = None
    enabled: bool = True
    password: str
    # Schrute Bucks balance. Earned via /mood check-ins, spent at /vending.
    points: int = 0
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), alias="updatedAt")
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), alias="createdAt")

    # More info at https://docs.pydantic.dev/latest/api/config/
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "591528c0-3029-4f8c-9aa8-fee16e271dbd",
                "name": "Dwight Schrute",
                "email": "dwight@dundermifflin.com",
                "birthdate": date.today(),
                "mood": Mood.happy,
                "enabled": True,
                "points": 0,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


class VendingItem(BaseModel):
    emoji: str
    name: str
    cost: int
