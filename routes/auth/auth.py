from fastapi import APIRouter
from dto.request import UserLoginRequest
import requests
        

router = APIRouter()

@router.post("/login")
async def login(user: UserLoginRequest):
    return await requests.post("")