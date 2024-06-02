from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Body, Depends, File, UploadFile, Query, Response
import requests
import os
from typing import Optional
from pydantic import BaseModel
from typing import List, Optional, Dict
from starlette import status

router = APIRouter(
  prefix="/meals",
  tags=["meals"]
)

load_dotenv()

api_url = os.getenv("MEALS_WORKOUTS_API_URL")

class MealBase(BaseModel):
  name: str
  calories: int
  carbs: float
  fat: float
  protein: float
  fiber: float
  sugar: float
  serving: Optional[int] = None
  image_url: Optional[str] = None

class MealCreate(BaseModel):
  name: str
  calories: int
  carbs: float
  fat: float
  protein: float
  fiber: float
  sugar: float
  serving: Optional[int] = None

  class Config:
    from_attributes = True
    orm_mode = True
        
class Meal(MealBase):
  id: int

  class Config:
    orm_mode = True
    from_attributes = True
    

# Routes
@router.get("/", response_model=List[Meal])
def get_meals(response: Response):
  response = requests.get(f"{api_url}/api/v1/meals")
  print(f"{api_url}/meals")
  print(response)
  if response.status_code == 200:
    return response.json()
  raise HTTPException(status_code=response.status_code, detail=response.json())

@router.get("/daily-meal-plan", response_model=List[Meal])
def get_daily_meal_plan(response: Response, type: str = None):
  response = requests.get(f"{api_url}/api/v1/meals/daily-meal-plan?type={type}")
  if response.status_code == 200:
    return response.json()
  raise HTTPException(status_code=response.status_code, detail=response.json())

@router.get("/weekly-meal-plan", response_model=Dict[str, List[Meal]])
def get_weekly_meal_plan(response: Response, type: str = None):
  response = requests.get(f"{api_url}/api/v1/meals/weekly-meal-plan?type={type}")
  if response.status_code == 200:
    return response.json()
  raise HTTPException(status_code=response.status_code, detail=response.json())

@router.get("/{meal_id}", response_model=Meal)
def get_meal(meal_id: int, response: Response):
  response = requests.get(f"{api_url}/api/v1/meals/{meal_id}")
  if response.status_code == 200:
    return response.json()
  raise HTTPException(status_code=response.status_code, detail=response.json())

@router.post("/", response_model=Meal)
def create_meal(response: Response, meal: MealCreate = Depends(), file: UploadFile = File(...)):
  response = requests.post(f"{api_url}/api/v1/meals", files={"file": (file.filename, file.file, file.content_type)}, data=meal.dict())
  if response.status_code == 201:
    return response.json()
  raise HTTPException(status_code=response.status_code, detail=response.json())

@router.put("/{meal_id}", response_model=Meal)
def update_meal(meal_id: int, meal: MealCreate, response: Response):
  response = requests.put(f"{api_url}/api/v1/meals/{meal_id}", json=meal.dict())
  if response.status_code == 200:
    return response.json()
  raise HTTPException(status_code=response.status_code, detail=response.json())

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, response: Response):
  response = requests.delete(f"{api_url}/api/v1/meals/{meal_id}")
  if response.status_code == 204:
    return response.text
  raise HTTPException(status_code=response.status_code, detail=response.json())