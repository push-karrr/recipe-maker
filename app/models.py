from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, autoincrement = True, primary_key = True)
    recipe_name = Column(String, nullable= False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    ingredients = relationship("Ingredient", backref = "recipe", cascade="all, delete-orphan")
    steps = relationship("Step", backref = "recipe", cascade="all, delete-orphan")
    users = relationship("Users", backref="recipe")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    ratings = Column(String, nullable = True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(String, nullable = False)
    quantity = Column(String, nullable = False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable = False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, autoincrement = True, primary_key = True)
    step_name = Column(String, nullable = False)
    duration = Column(String, nullable = False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable = False   )
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))