from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import io, csv

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
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    crud.create_meal(db, schemas.MealCreate(foods=foods, notes=notes))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# Drink form handler
@router.post("/drinks/form")
def create_drink_form(
    type: str = Form(...),
    volume_ml: float = Form(...),
    caffeine: Optional[int] = Form(0),
    alcohol: Optional[int] = Form(0),
    db: Session = Depends(get_db)
):
    crud.create_drink(db, schemas.DrinkCreate(
        type=type,
        volume_ml=volume_ml,
        caffeine=int(caffeine) if caffeine is not None else 0,
        alcohol=int(alcohol) if alcohol is not None else 0
    ))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# Bowel Movement form handler
@router.post("/bowel-movements/form")
def create_bm_form(
    bristol_scale: int = Form(...),
    urgency: Optional[int] = Form(None),
    pain: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    crud.create_bm(db, schemas.BowelMovementCreate(
        bristol_scale=bristol_scale, urgency=urgency, pain=pain, notes=notes
    ))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# Feelings form handler
@router.post("/feelings/form")
def create_feeling_form(
    stress: Optional[int] = Form(None),
    anxiety: Optional[int] = Form(None),
    sleep_quality: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    crud.create_feeling(db, schemas.FeelingCreate(
        stress=stress, anxiety=anxiety, sleep_quality=sleep_quality, notes=notes
    ))
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# ---------------- DASHBOARD ----------------

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# ---------------- EXPORT ----------------

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(["type", "timestamp", "field1", "field2", "field3", "notes"])

    # Meals
    for m in crud.get_meals(db):
        writer.writerow(["meal", m.timestamp, m.foods, "", "", m.notes or ""])

    # Drinks
    for d in crud.get_drinks(db):
        writer.writerow(["drink", d.timestamp, d.type, d.volume_ml, f"C:{d.caffeine}/A:{d.alcohol}", ""])

    # Bowel Movements
    for b in crud.get_bms(db):
        writer.writerow(["bowel", b.timestamp, b.bristol_scale, b.urgency, b.pain, b.notes or ""])

    # Feelings
    for f in crud.get_feelings(db):
        writer.writerow(["feeling", f.timestamp, f.stress, f.anxiety, f.sleep_quality, f.notes or ""])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tracker_data.csv"}
    )
