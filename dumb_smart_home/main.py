from pathlib import Path
from typing import Optional

import uvicorn
from ac_handler import router as ac_router
from auth import get_auth
from auth import router as auth_router
from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.include_router(auth_router)
app.include_router(ac_router)

app.mount("/static", StaticFiles(directory=Path(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@app.api_route("/", methods=["GET", "POST"], status_code=200)
def root(request: Request, cookie: Optional[dict] = Depends(get_auth)) -> Response:
    template = "login.html" if not cookie else "control.html"
    return templates.TemplateResponse(template, {"request": request})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=7654,
        reload=True,
    )
