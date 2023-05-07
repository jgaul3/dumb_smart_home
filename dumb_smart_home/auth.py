import os
import time
from typing import Optional

import jwt
from fastapi import APIRouter, Cookie, Form
from jwt import PyJWTError
from starlette.responses import RedirectResponse

router = APIRouter()


def gen_auth() -> str:
    return jwt.encode(
        {"made_at": int(time.time())}, key=os.getenv("SECRET"), algorithm="HS256"
    )


def get_auth(cookie: str = Cookie("")) -> Optional[dict]:
    try:
        return jwt.decode(cookie, key=os.getenv("SECRET"), algorithms=["HS256"])
    except PyJWTError:
        return None


@router.post("/authenticate", response_class=RedirectResponse)
def authenticate(access_key: str = Form(...)):
    response = RedirectResponse("/")
    if access_key == "asdf":
        # if access_key == os.getenv("DEFAULT_PASSWORD"):
        response.set_cookie(key="cookie", value=gen_auth(), secure=True, httponly=True)

    return response


@router.get("/logout", response_class=RedirectResponse)
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("cookie")
    return response
