from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---------- Meals ----------
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

# ---------- Drinks ----------
class DrinkBase(BaseModel):
    type: str
    volume_ml: float
    caffeine: Optional[int] = 0
    alcohol: Optional[int] = 0

class DrinkCreate(DrinkBase):
    pass

class Drink(DrinkBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

# ---------- Bowel Movements ----------
class BowelMovementBase(BaseModel):
    bristol_scale: int
    urgency: Optional[int] = None
    pain: Optional[int] = None
    notes: Optional[str] = None

class BowelMovementCreate(BowelMovementBase):
    pass

class BowelMovement(BowelMovementBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

# ---------- Feelings ----------
class FeelingBase(BaseModel):
    stress: Optional[int] = None
    anxiety: Optional[int] = None
    sleep_quality: Optional[int] = None
    notes: Optional[str] = None

class FeelingCreate(FeelingBase):
    pass

class Feeling(FeelingBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True
