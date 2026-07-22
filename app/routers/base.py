from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.models import Login
from app.services import user as service
from app.utils import auth

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", encoding="utf8") as file:
        return HTMLResponse(content=file.read().rstrip(), status_code=200)


@router.post("/auth")
async def get_token(login: Login):
    user = await service.find(email=login.username, include_password=True)
    if not user or not auth.check_password(plain=login.password, hashed=user.get("password")):
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    return auth.create_token(subject=user.get("email"), mood=user.get("mood", ""))
