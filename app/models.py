from datetime import date, datetime
from enum import Enum
from typing import Annotated, Any, Optional

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
    mood: Optional[Mood] = None
    enabled: bool = True
    password: str
    updated_at: Optional[datetime] = Field(datetime.utcnow(), alias="updatedAt")
    created_at: Optional[datetime] = Field(datetime.utcnow(), alias="createdAt")

    # More info at https://docs.pydantic.dev/latest/api/config/
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "591528c0-3029-4f8c-9aa8-fee16e271dbd",
                "name": "Anthony",
                "email": "anthony@github.com",
                "birthdate": date.today(),
                "mood": Mood.happy,
                "enabled": True,
                "updated_at": datetime.utcnow(),
            }
        },
    )
