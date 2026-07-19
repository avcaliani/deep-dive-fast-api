from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class Mood(str, Enum):
    happy = "😁"
    angry = "😡"
    insightful = "🤔"


class UUID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ID!")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema: Any):
        field_schema.update(type="string")


class User(BaseModel):
    id: UUID = Field(default_factory=UUID, alias="_id")
    name: str
    email: EmailStr
    birthdate: date
    mood: Optional[Mood] = None
    enabled: bool = True
    password: str
    updated_at: Optional[datetime] = Field(datetime.utcnow(), alias="updatedAt")
    created_at: Optional[datetime] = Field(datetime.utcnow(), alias="createdAt")

    class Config:
        # More info at https://pydantic-docs.helpmanual.io/usage/model_config/
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "591528c0-3029-4f8c-9aa8-fee16e271dbd",
                "name": "Anthony",
                "email": "anthony@github.com",
                "birthdate": date.today(),
                "mood": Mood.happy,
                "enabled": True,
                "updated_at": datetime.utcnow(),
            }
        }
