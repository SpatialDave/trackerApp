from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    meals = relationship("Meal", back_populates="owner")
    drinks = relationship("Drink", back_populates="owner")
    bowel_movements = relationship("BowelMovement", back_populates="owner")
    feelings = relationship("Feeling", back_populates="owner")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    foods = Column(Text)
    notes = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="meals")

class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String)
    volume_ml = Column(Float)
    caffeine = Column(Integer, default=0)
    alcohol = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="drinks")

class BowelMovement(Base):
    __tablename__ = "bowel_movements"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    bristol_scale = Column(Integer)
    urgency = Column(Integer)
    pain = Column(Integer)
    notes = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bowel_movements")

class Feeling(Base):
    __tablename__ = "feelings"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    stress = Column(Integer)
    anxiety = Column(Integer)
    sleep_quality = Column(Integer)
    notes = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="feelings")
