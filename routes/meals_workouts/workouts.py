from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    HTTPException,
    Body,
    Depends,
    File,
    UploadFile,
    Query,
    Response,
    Form,
)
import requests
import os
from typing import Optional
from pydantic import BaseModel
from typing import List, Optional, Dict
from starlette import status

router = APIRouter(prefix="/workouts", tags=["workouts"])

load_dotenv()

api_url = os.getenv("MEALS_WORKOUTS_API_URL")


class ExerciseBase(BaseModel):
    name: str
    reps: Optional[int] = None
    sets: Optional[int] = None
    duration: Optional[int] = None  # Duration in seconds


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int
    workout_id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True


class WorkoutBase(BaseModel):
    name: str
    description: str
    duration: int
    calories: int
    type: str
    difficulty: str


class WorkoutCreate(WorkoutBase):
    exercises: List[ExerciseCreate]


class Workout(WorkoutBase):
    id: int
    image_url: Optional[str] = None
    exercises: List[Exercise] = []

    class Config:
        from_attributes = True
        orm_mode = True


class WorkoutUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    duration: Optional[int]
    calories: Optional[int]
    type: Optional[str]
    difficulty: Optional[str]


# Routes


@router.get("/", response_model=List[Workout])
def get_workouts(response: Response):
    response = requests.get(f"{api_url}/api/v1/workouts")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.get("/{workout_id}", response_model=Workout)
def get_workout(workout_id: int, response: Response):
    response = requests.get(f"{api_url}/api/v1/workouts/{workout_id}")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Workout)
def create_workout(
    response: Response,
    name: str = Form(...),
    description: str = Form(...),
    duration: int = Form(...),
    calories: int = Form(...),
    type: str = Form(...),
    difficulty: str = Form(...),
    file: UploadFile = File(None),
):
    response = requests.post(
        f"{api_url}/api/v1/workouts",
        data={
            "name": name,
            "description": description,
            "duration": duration,
            "calories": calories,
            "type": type,
            "difficulty": difficulty,
        },
        files={"file": (file.filename, file.file, file.content_type)},
    )
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.put("/{workout_id}")
def update_workout(workout_id: int, workout_update: WorkoutUpdate):
    response = requests.put(
        f"{api_url}/api/v1/workouts/{workout_id}", json=workout_update.dict()
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.delete("/{workout_id}")
def delete_workout(workout_id: int):
    response = requests.delete(f"{api_url}/api/v1/workouts/{workout_id}")
    if response.status_code == 204:
        return response.text
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.get("/{type}/{difficulty}", response_model=List[Workout])
def get_workouts_by_type_and_difficulty(type: str, difficulty: str):
    response = requests.get(f"{api_url}/api/v1/workouts/{type}/{difficulty}")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.post("/exercises/", response_model=Exercise)
def create_exercise(
    exercise: ExerciseCreate,
    workout_id: int = Form(...),
    name: str = Form(...),
    reps: int = Form(None),
    sets: int = Form(None),
    duration: int = Form(None),
    file: UploadFile = File(None),
):
    response = requests.post(
        f"{api_url}/api/v1/workouts/exercises", json=exercise.dict()
    )
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())
