from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime
from .database import Base

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    foods = Column(Text)
    notes = Column(Text)

class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String)
    volume_ml = Column(Float)
    caffeine = Column(Integer, default=0)
    alcohol = Column(Integer, default=0)

class BowelMovement(Base):
    __tablename__ = "bowel_movements"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    bristol_scale = Column(Integer)
    urgency = Column(Integer)
    pain = Column(Integer)
    notes = Column(Text)

class Feeling(Base):
    __tablename__ = "feelings"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    stress = Column(Integer)
    anxiety = Column(Integer)
    sleep_quality = Column(Integer)
    notes = Column(Text)
