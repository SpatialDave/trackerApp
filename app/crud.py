from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def create_meal(db: Session, meal: schemas.MealCreate):
    db_meal = models.Meal(
        foods=meal.foods,
        notes=meal.notes,
        timestamp=datetime.utcnow()
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def get_meals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meal).offset(skip).limit(limit).all()
