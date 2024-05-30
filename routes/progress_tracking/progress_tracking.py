from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import requests
import os
import dataclasses
from dataclasses import dataclass, asdict
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
    is_completed: Optional[bool] = None

@dataclass
class UserProgressBase:
    user_id: int

@dataclass
class UserProgressCreate(UserProgressBase):
    pass

########################################### methods ###########################################

def serialize_goal(goal) -> dict:
    goal_dict = asdict(goal)
    if goal_dict['goal_type']:
        goal_dict['goal_type'] = goal_dict['goal_type'].value
    if goal_dict['period_unit']:
        goal_dict['period_unit'] = goal_dict['period_unit'].value
    
    return {k: v for k, v in goal_dict.items() if v is not None}

@router.post("/goals/new-goal/")
def add_goal(goal: GoalCreate):
    goal_data = serialize_goal(goal)
    result = requests.post(api_url + "/api/v1/goals/new-goal", json=goal_data)
    if result.status_code == 201:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.put("/goals/{goal_id}/update-goal/")
def update_goal(goal_id: int, goal_update: GoalUpdate):
    goal_data = serialize_goal(goal_update)
    result = requests.put(api_url + f"/api/v1/goals/{goal_id}/update-goal/", json=goal_data)
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.delete("/goals/{goal_id}/delete-goal/")
def delete_goal(goal_id: int):
    result = requests.delete(api_url + f"/api/v1/goals/{goal_id}/delete-goal/")
    if result.status_code == 200:
        return result.text
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/goals/{goal_id}/")
def get_goal(goal_id: int):
    result = requests.get(api_url + f"/api/v1/goals/{goal_id}/")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/{user_id}/goals/")
def get_all_user_goal(user_id: int):
    result = requests.get(api_url + f"/api/v1/{user_id}/goals/")
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
def update_user_progress(user_id: int):
    result = requests.put(api_url + f"/api/v1/{user_id}/update-progress/")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.delete("/{user_id}/clear-progress/")
def clear_user_progress(user_id: int):
    result = requests.delete(api_url + f"/api/v1/{user_id}/clear-progress/")
    if result.status_code == 200:
        return result.text
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))

@router.get("/{user_id}/progress/")
def get_user_progress(user_id: int):
    result = requests.get(api_url + f"/api/v1/{user_id}/progress/")
    if result.status_code == 200:
        return result.json()
    raise HTTPException(status_code=result.status_code, detail=result.json().get("message"))