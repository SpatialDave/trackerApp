from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

# ---------- Meals ----------
def create_meal(db: Session, meal: schemas.MealCreate):
    db_meal = models.Meal(**meal.dict(), timestamp=datetime.utcnow())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def get_meals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meal).offset(skip).limit(limit).all()

# ---------- Drinks ----------
def create_drink(db: Session, drink: schemas.DrinkCreate):
    db_drink = models.Drink(**drink.dict(), timestamp=datetime.utcnow())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink

def get_drinks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Drink).offset(skip).limit(limit).all()

# ---------- Bowel Movements ----------
def create_bm(db: Session, bm: schemas.BowelMovementCreate):
    db_bm = models.BowelMovement(**bm.dict(), timestamp=datetime.utcnow())
    db.add(db_bm)
    db.commit()
    db.refresh(db_bm)
    return db_bm

def get_bms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BowelMovement).offset(skip).limit(limit).all()

# ---------- Feelings ----------
def create_feeling(db: Session, feeling: schemas.FeelingCreate):
    db_feeling = models.Feeling(**feeling.dict(), timestamp=datetime.utcnow())
    db.add(db_feeling)
    db.commit()
    db.refresh(db_feeling)
    return db_feeling

def get_feelings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feeling).offset(skip).limit(limit).all()
