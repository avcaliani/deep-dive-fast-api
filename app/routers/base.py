from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.services import user as service
from app.utils import auth

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", encoding="utf8") as file:
        return HTMLResponse(content=file.read().rstrip(), status_code=200)


@router.post("/auth")
async def get_token(form: OAuth2PasswordRequestForm = Depends()):
    # Here, I'm using OAuth2PasswordRequestForm to retrieve user and password.
    # But, let's say that you want to receive a JSON in a custom format, then
    # you just have to change OAuth2PasswordRequestForm by your Pydantic Entity.
    # Something like...
    #
    # class Login(BaseModel):
    #     username: str
    #     password: str
    #
    # async def get_token(login: Login): ...
    user = await service.find(email=form.username)
    password_ok = auth.check_password(plain=form.password, hashed=user.get("password"))
    if not user or not password_ok:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    return auth.create_token(subject=user.get("email"), mood=user.get("mood", ""))
