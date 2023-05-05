import os
import time
from pathlib import Path
from typing import Optional

import jwt
import uvicorn
from fastapi import Cookie, Depends, FastAPI, Form
from fastapi.templating import Jinja2Templates
from jwt import PyJWTError
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


def gen_auth() -> str:
    return jwt.encode(
        {"made_at": int(time.time())}, key=os.getenv("SECRET"), algorithm="HS256"
    )


def get_auth(cookie: str = Cookie("")) -> Optional[dict]:
    try:
        return jwt.decode(cookie, key=os.getenv("SECRET"), algorithms=["HS256"])
    except PyJWTError:
        return None


@app.api_route("/", methods=["GET", "POST"], status_code=200)
def root(request: Request, cookie: dict = Depends(get_auth)) -> Response:
    template = "login.html" if not cookie else "control.html"
    return templates.TemplateResponse(template, {"request": request})


@app.post("/authenticate", response_class=RedirectResponse)
def authenticate(access_key: str = Form(...)):
    response = RedirectResponse("/")
    if access_key == "asdf":
        # if access_key == os.getenv("DEFAULT_PASSWORD"):
        response.set_cookie(key="cookie", value=gen_auth(), secure=True, httponly=True)

    return response


@app.get("/logout", response_class=RedirectResponse)
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("cookie")
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=7654,
        reload=True,
    )
