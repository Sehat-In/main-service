import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import APIRouter
from routes.auth import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

router1 = APIRouter()

@router1.get("")
async def hello():
    return {"message": "Hello World"}

app.include_router(router1, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")  
