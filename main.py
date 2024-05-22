from fastapi import FastAPI
from fastapi import APIRouter
from routes.auth import auth

app = FastAPI()

router1 = APIRouter()
app.include_router(router1, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")

@router1.get("/hello")
async def hello():
    return {"message": "Hello World"}
