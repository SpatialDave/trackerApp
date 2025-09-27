from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- API ENDPOINTS ----------------

# Meals
@router.post("/meals/", response_model=schemas.Meal)
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db)):
    return crud.create_meal(db=db, meal=meal)

@router.get("/meals/", response_model=List[schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_meals(db, skip=skip, limit=limit)

# Drinks
@router.post("/drinks/", response_model=schemas.Drink)
def create_drink(drink: schemas.DrinkCreate, db: Session = Depends(get_db)):
    return crud.create_drink(db=db, drink=drink)

@router.get("/drinks/", response_model=List[schemas.Drink])
def read_drinks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_drinks(db, skip=skip, limit=limit)

# Bowel Movements
@router.post("/bowel-movements/", response_model=schemas.BowelMovement)
def create_bm(bm: schemas.BowelMovementCreate, db: Session = Depends(get_db)):
    return crud.create_bm(db=db, bm=bm)

@router.get("/bowel-movements/", response_model=List[schemas.BowelMovement])
def read_bms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bms(db, skip=skip, limit=limit)

# Feelings
@router.post("/feelings/", response_model=schemas.Feeling)
def create_feeling(feeling: schemas.FeelingCreate, db: Session = Depends(get_db)):
    return crud.create_feeling(db=db, feeling=feeling)

@router.get("/feelings/", response_model=List[schemas.Feeling])
def read_feelings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_feelings(db, skip=skip, limit=limit)

# ---------------- FRONT-END FORMS ----------------

@router.get("/form", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Meal form handler
@router.post("/meals/form")
def create_meal_form(
    foods: str = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    crud.create_meal(db, schemas.MealCreate(foods=foods, notes=notes))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# Drink form handler
@router.post("/drinks/form")
def create_drink_form(
    type: str = Form(...),
    volume_ml: float = Form(...),
    caffeine: int = Form(0),
    alcohol: int = Form(0),
    db: Session = Depends(get_db)
):
    crud.create_drink(db, schemas.DrinkCreate(
        type=type, volume_ml=volume_ml, caffeine=caffeine, alcohol=alcohol
    ))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# Bowel Movement form handler
@router.post("/bowel-movements/form")
def create_bm_form(
    bristol_scale: int = Form(...),
    urgency: int = Form(None),
    pain: int = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    crud.create_bm(db, schemas.BowelMovementCreate(
        bristol_scale=bristol_scale, urgency=urgency, pain=pain, notes=notes
    ))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# Feelings form handler
@router.post("/feelings/form")
def create_feeling_form(
    stress: int = Form(None),
    anxiety: int = Form(None),
    sleep_quality: int = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    crud.create_feeling(db, schemas.FeelingCreate(
        stress=stress, anxiety=anxiety, sleep_quality=sleep_quality, notes=notes
    ))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)
