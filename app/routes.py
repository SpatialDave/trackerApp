from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Meals ----------
@router.post("/meals/", response_model=schemas.Meal)
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db)):
    return crud.create_meal(db=db, meal=meal)

@router.get("/meals/", response_model=List[schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_meals(db, skip=skip, limit=limit)

# ---------- Drinks ----------
@router.post("/drinks/", response_model=schemas.Drink)
def create_drink(drink: schemas.DrinkCreate, db: Session = Depends(get_db)):
    return crud.create_drink(db=db, drink=drink)

@router.get("/drinks/", response_model=List[schemas.Drink])
def read_drinks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_drinks(db, skip=skip, limit=limit)

# ---------- Bowel Movements ----------
@router.post("/bowel-movements/", response_model=schemas.BowelMovement)
def create_bm(bm: schemas.BowelMovementCreate, db: Session = Depends(get_db)):
    return crud.create_bm(db=db, bm=bm)

@router.get("/bowel-movements/", response_model=List[schemas.BowelMovement])
def read_bms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bms(db, skip=skip, limit=limit)

# ---------- Feelings ----------
@router.post("/feelings/", response_model=schemas.Feeling)
def create_feeling(feeling: schemas.FeelingCreate, db: Session = Depends(get_db)):
    return crud.create_feeling(db=db, feeling=feeling)

@router.get("/feelings/", response_model=List[schemas.Feeling])
def read_feelings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_feelings(db, skip=skip, limit=limit)
