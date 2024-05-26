from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response
import requests
import os
import dataclasses
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

router = APIRouter()

load_dotenv()

api_url = os.getenv("PROGRESS_API_URL")

########################################### dataclasses ###########################################

class GoalType(Enum):
    WEIGHTLOSS = "lose_weight"
    WEIGHTGAIN = "gain_weight"
    CALORIEINTAKE = "calorie_intake"
    CALORIEBURNED = "calorie_burned"

class PeriodUnit(Enum):
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"
    YEAR = "year"

@dataclass
class GoalBase:
    user_id: int
    goal_type: GoalType
    value: float
    period: int
    period_unit: PeriodUnit
    progress: Optional[float] = 0.0
    progress_percentage: Optional[float] = 0.0
    is_completed: Optional[bool] = False

@dataclass
class GoalCreate(GoalBase):
    pass

@dataclass
class GoalUpdate:
    goal_type: Optional[GoalType] = None
    value: Optional[float] = None
    period: Optional[int] = None
    period_unit: Optional[PeriodUnit] = None
    progress: Optional[float] = None
    progress_percentage: Optional[float] = None
    is_completed: Optional[bool] = None

@dataclass
class UserProgressBase:
    user_id: int
    overall_progress_percentage: Optional[float] = 0.0

@dataclass
class UserProgressCreate(UserProgressBase):
    pass

@dataclass
class UserProgressUpdate:
    overall_progress_percentage: float

########################################### methods ###########################################

@router.post("/goals/new-goal/")
def add_goal(goal: GoalCreate):
    result = requests.post(api_url + "/api/v1/goals/new-goal", json=dataclasses.asdict(goal))
    if result.status_code == 201:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.put("/goals/{goal_id}/update-goal/")
def update_goal(goal_id: int, goal_update: GoalUpdate):
    result = requests.post(api_url + f"/api/v1/goals/{goal_id}/update-goal/", json=dataclasses.asdict(goal_update))
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.delete("/goals/{goal_id}/delete-goal/")
def delete_goal(goal_id: int):
    result = requests.post(api_url + f"/api/v1/goals/{goal_id}/delete-goal/")
    if result.status_code == 200:
        return result.text
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/goals/{goal_id}/")
def get_goal(goal_id: int):
    result = requests.post(api_url + f"/api/v1/goals/{goal_id}/")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/{user_id}/goals/")
def get_all_user_goal(user_id: int):
    result = requests.post(api_url + f"/api/v1/{user_id}/goals/")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.post("/create-progress/")
def create_user_progress(user_progress: UserProgressCreate):
    result = requests.post(api_url + "/api/v1/create-progress/", json=dataclasses.asdict(user_progress))
    if result.status_code == 201:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.put("/{user_id}/update-progress/")
def update_user_progress(user_id: int, user_progress_update: UserProgressUpdate):
    result = requests.post(api_url + f"/api/v1/{user_id}/update-progress/", json=dataclasses.asdict(user_progress_update))
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.delete("/{user_id}/clear-progress/")
def clear_user_progress(user_id: int):
    result = requests.post(api_url + f"/api/v1/{user_id}/clear-progress/")
    if result.status_code == 200:
        return result.text
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/{user_id}/progress/")
def get_user_progress(user_id: int):
    result = requests.post(api_url + f"/api/v1/{user_id}/progress/")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))