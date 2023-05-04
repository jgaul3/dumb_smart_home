import uvicorn
from fastapi import APIRouter, FastAPI

app = FastAPI()

router = APIRouter()


@router.get("/", status_code=200)
def root() -> dict:
    return {"msg": "Hello World!"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=7654,
        reload=True,
    )
