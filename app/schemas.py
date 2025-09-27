from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MealBase(BaseModel):
    foods: str
    notes: Optional[str] = None

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
