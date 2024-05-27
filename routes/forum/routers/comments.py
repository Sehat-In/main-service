from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import requests
import os

router = APIRouter()

load_dotenv()

api_url = os.getenv("FORUM_API_URL")

class CommentRequest(BaseModel):
    content: str
    username: str

@router.get("/get/{comment_id}")
async def get_comment(comment_id: str):
    result = requests.get(api_url + f"/api/v1/comments/get/{comment_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.post("/create")
async def create_comment(comment: CommentRequest):
    result = requests.post(api_url + f"/api/v1/comments/create", json=comment.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.delete("/delete/{comment_id}")
async def delete_comment(comment_id: str):
    result = requests.delete(api_url + f"/api/v1/comments/delete/{comment_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.put("/update/{comment_id}")
async def update_comment(comment_id: str):
    result = requests.put(api_url + f"/api/v1/comments/update/{comment_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())