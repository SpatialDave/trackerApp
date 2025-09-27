from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database
from .routes import router

# Create tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="IBS Tracker")

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
