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

class CommentUpdateRequest(BaseModel):
    content: str

@router.get("/get/{comment_id}")
async def get_comment(comment_id: str):
    result = requests.get(api_url + f"/api/v1/comments/get/{comment_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.post("/create/{post_id}")
async def create_comment(post_id: str, comment: CommentRequest):
    result = requests.post(api_url + f"/api/v1/comments/create/{post_id}", json=comment.model_dump())
    print(result)
    if result.status_code == 201:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.delete("/delete/{comment_id}")
async def delete_comment(comment_id: str):
    result = requests.delete(api_url + f"/api/v1/comments/delete/{comment_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.put("/update/{comment_id}")
async def update_comment(comment_id: str, comment: CommentUpdateRequest):
    result = requests.put(api_url + f"/api/v1/comments/update/{comment_id}", json=comment.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())