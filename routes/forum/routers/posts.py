from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import requests
import os

router = APIRouter()

load_dotenv()

api_url = os.getenv("FORUM_API_URL")

class PostRequest(BaseModel):
    title: str
    content: str
    username: str

class PostUpdateRequest(BaseModel):
    title: str
    content: str

class SubscribeRequest(BaseModel):
    username: str
    post_id: str

@router.get("/get/all")
async def get_all_post():
    result = requests.get(api_url + f"/api/v1/posts/get/all")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.get("/get/{post_id}")
async def get_post(post_id: str):
    result = requests.get(api_url + f"/api/v1/posts/get/{post_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.post("/create")
async def create_post(post: PostRequest):
    result = requests.post(api_url + f"/api/v1/posts/create", json=post.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.delete("/delete/{post_id}")
async def delete_post(post_id: str):
    result = requests.delete(api_url + f"/api/v1/posts/delete/{post_id}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())

@router.put("/update/{post_id}")
async def update_post(post_id: str, post: PostUpdateRequest):
    result = requests.put(api_url + f"/api/v1/posts/update/{post_id}", json=post.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json())


@router.get("/check-notification/{username}")
async def check_notification(username: str):
    result = requests.get(api_url + f"/api/v1/posts/check-notification/{username}")
    if result.status_code == 200:
        return result.text
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/get-notifications/{username}")
async def get_notifications(username: str):
    result = requests.get(api_url + f"/api/v1/posts/get-notifications/{username}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/remove-notifications/{username}")
async def remove_notifications(username: str):
    result = requests.get(api_url + f"/api/v1/posts/remove-notifications/{username}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.post("/subscribe")
async def subscribe(request: SubscribeRequest):
    result = requests.post(api_url + f"/api/v1/posts/subscribe", json=request.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.delete("/unsubscribe")
async def subscribe(request: SubscribeRequest):
    result = requests.delete(api_url + f"/api/v1/posts/unsubscribe", json=request.model_dump())
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/get-subscriptions/{username}")
async def get_subscriptions(username: str):
    result = requests.get(api_url + f"/api/v1/posts/get-subscriptions/{username}")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))