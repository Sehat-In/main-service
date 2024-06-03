from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import requests
import os

router = APIRouter()

load_dotenv()

api_url = os.getenv("FORUM_API_URL")

class LikeRequest(BaseModel):
    post_id: str
    username: str

class UserRequest(BaseModel):
    username: str

@router.get("/get/{post_id}")
async def get_likes(post_id: str):
    result = requests.get(api_url + f"/api/v1/likes/get/{post_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.get("/get/count/{post_id}")
async def get_likes_count(post_id: str):
    result = requests.get(api_url + f"/api/v1/likes/get/count/{post_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.post("/like/{post_id}")
async def like_post(post_id: str, like: UserRequest):
    result = requests.post(api_url + f"/api/v1/likes/add/{post_id}", json=like.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.delete("/unlike/{post_id}")
async def remove_like(post_id: str, like: UserRequest):
    result = requests.delete(api_url + f"/api/v1/likes/remove/{post_id}", json=like.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.post("/get-user/{post_id}")
async def get_user_like(post_id: str, like: UserRequest):
    result = requests.post(api_url + f"/api/v1/likes/get-user/{post_id}", json=like.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())