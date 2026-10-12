from fastapi import APIRouter, Depends, HTTPException

from app import dependencies
from app.models import User
from app.services import user as service

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(dependencies.get_user)])


@router.get("/me")
async def who_am_i(user: dict = Depends(dependencies.get_user)):
    return user


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await service.find(id_=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found!")
    return user


@router.post("/", status_code=201)
async def create_user(user: User):
    return await service.create(user)
