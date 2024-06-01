from dataclasses import dataclass
import dataclasses
from dotenv import load_dotenv
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import os

@dataclass
class UserRequest(BaseModel):
    username: str
    password: str

router = APIRouter()

load_dotenv()

api_url = os.getenv("AUTH_API_URL") + "/api/v1/auth"
api_url_progress = os.getenv("PROGRESS_API_URL")

@router.get("/login-google")
async def login_google():
    return RedirectResponse(api_url + "/login-google")

@router.post("/login")
async def login(user: UserRequest):
    result = requests.post(api_url + "/login", json=dataclasses.asdict(user))
    if (result.status_code != 201):
        raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))    
    temp = requests.post(api_url_progress + f"/api/v1/{result.json().get("id")}/create-progress")
    if (temp.status_code != 201):
        raise HTTPException(status_code=temp.status_code, detail=temp.json().get("detail"))   
    return result.json()

@router.post("/register")
async def register(user: UserRequest):
    result = requests.post(api_url + "/register", json=dataclasses.asdict(user))
    if (result.status_code == 201):
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/refresh")
async def refresh(request: Request):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = request.headers["Authorization"]
    result = requests.get(api_url + "/refresh", headers={"Authorization": token})
    if (result.status_code == 200):
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/get-data-from-token")
async def get_data_from_token(request: Request):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = request.headers["Authorization"]
    result = requests.get(api_url + "/get-data-from-token", headers={"Authorization": token})
    if (result.status_code == 200):
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))


