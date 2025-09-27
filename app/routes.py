from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import io, csv

from . import crud, schemas, database, models
from .auth import authenticate_user, create_access_token, get_current_user_from_cookie, get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- AUTH PAGES ----------------

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/form", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", token, httponly=True, max_age=60*60*24, samesite="lax")
    return response

@router.post("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

# ---------------- API ENDPOINTS (protected) ----------------

@router.post("/meals/", response_model=schemas.Meal)
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.create_meal(db=db, meal=meal, user_id=current_user.id)

@router.get("/meals/", response_model=List[schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.get_meals(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/drinks/", response_model=schemas.Drink)
def create_drink(drink: schemas.DrinkCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.create_drink(db=db, drink=drink, user_id=current_user.id)

@router.get("/drinks/", response_model=List[schemas.Drink])
def read_drinks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.get_drinks(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/bowel-movements/", response_model=schemas.BowelMovement)
def create_bm(bm: schemas.BowelMovementCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.create_bm(db=db, bm=bm, user_id=current_user.id)

@router.get("/bowel-movements/", response_model=List[schemas.BowelMovement])
def read_bms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.get_bms(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/feelings/", response_model=schemas.Feeling)
def create_feeling(feeling: schemas.FeelingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.create_feeling(db=db, feeling=feeling, user_id=current_user.id)

@router.get("/feelings/", response_model=List[schemas.Feeling])
def read_feelings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    return crud.get_feelings(db, user_id=current_user.id, skip=skip, limit=limit)

# ---------------- FRONT-END FORMS (protected) ----------------

@router.get("/form", response_class=HTMLResponse)
def form_page(request: Request, current_user: models.User = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/meals/form")
def create_meal_form(foods: str = Form(...), notes: Optional[str] = Form(None), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    crud.create_meal(db, schemas.MealCreate(foods=foods, notes=notes), user_id=current_user.id)
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/drinks/form")
def create_drink_form(type: str = Form(...), volume_ml: float = Form(...), caffeine: Optional[int] = Form(0), alcohol: Optional[int] = Form(0), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    crud.create_drink(db, schemas.DrinkCreate(
        type=type,
        volume_ml=volume_ml,
        caffeine=int(caffeine) if caffeine is not None else 0,
        alcohol=int(alcohol) if alcohol is not None else 0
    ), user_id=current_user.id)
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/bowel-movements/form")
def create_bm_form(bristol_scale: int = Form(...), urgency: Optional[int] = Form(None), pain: Optional[int] = Form(None), notes: Optional[str] = Form(None), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    crud.create_bm(db, schemas.BowelMovementCreate(
        bristol_scale=bristol_scale, urgency=urgency, pain=pain, notes=notes
    ), user_id=current_user.id)
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/feelings/form")
def create_feeling_form(stress: Optional[int] = Form(None), anxiety: Optional[int] = Form(None), sleep_quality: Optional[int] = Form(None), notes: Optional[str] = Form(None), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    crud.create_feeling(db, schemas.FeelingCreate(
        stress=stress, anxiety=anxiety, sleep_quality=sleep_quality, notes=notes
    ), user_id=current_user.id)
    return RedirectResponse("/form", status_code=status.HTTP_303_SEE_OTHER)

# ---------------- DASHBOARD (protected) ----------------

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, current_user: models.User = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# ---------------- EXPORT (protected) ----------------

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_from_cookie)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["type", "timestamp", "field1", "field2", "field3", "notes"])

    for m in crud.get_meals(db, user_id=current_user.id):
        writer.writerow(["meal", m.timestamp, m.foods, "", "", m.notes or ""])
    for d in crud.get_drinks(db, user_id=current_user.id):
        writer.writerow(["drink", d.timestamp, d.type, d.volume_ml, f"C:{d.caffeine}/A:{d.alcohol}", ""])
    for b in crud.get_bms(db, user_id=current_user.id):
        writer.writerow(["bowel", b.timestamp, b.bristol_scale, b.urgency, b.pain, b.notes or ""])
    for f in crud.get_feelings(db, user_id=current_user.id):
        writer.writerow(["feeling", f.timestamp, f.stress, f.anxiety, f.sleep_quality, f.notes or ""])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=tracker_data.csv"})

