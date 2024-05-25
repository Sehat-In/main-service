from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response
import requests
import os

router = APIRouter()

load_dotenv()

api_url = os.getenv("FORUM_API_URL")

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
