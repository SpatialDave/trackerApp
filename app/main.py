from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database
from .routes import router

# Create tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="IBS Tracker")
templates = Jinja2Templates(directory="app/templates")
app.include_router(router)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, IBS Tracker is running!"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Just a quick DB check
    return {"status": "ok"}
