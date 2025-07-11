from typing import List, Optional

from pydantic import BaseModel, Field

class IngredientBase(BaseModel):
    name: str = Field(..., examples= ["Water"])
    quantity: str = Field(..., examples = ["1 cup"])

class IngredientCreate(IngredientBase):
    id: Optional[int] = None

class IngredientResponse(IngredientBase):
    id: int

    model_config = {
        "from_attributes": True
    }
class IngredientUpdate(IngredientBase):
    id:Optional[int] = None
    name: Optional[str] = None
    quantity:Optional[str] = None


class StepBase(BaseModel):
    step_name:Optional[str] = Field(..., examples= ["Boil Water"])
    duration:Optional[str] = Field(..., examples = ["1 minute"])

class StepCreate(StepBase):
    id : Optional[int] = None

class StepResponse(StepBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class StepUpdate(StepBase):
    id: Optional[int] = None


class RecipeBase(BaseModel):
    recipe_name:str = Field(..., examples= ["Maggi"])

class CreateRecipe(RecipeBase):
    ingredients: List[IngredientCreate]
    steps: List[StepCreate] = Field(...)

class UpdateRecipe(RecipeBase):
    recipe_name: Optional[str]
    ingredients: Optional[List[IngredientUpdate]] = None
    steps: Optional[List[StepUpdate]] = None

class RecipeResponse(RecipeBase):
    id: int
    ingredients : List[IngredientResponse]
    steps : List[StepResponse]

    model_config = {
        "from_attributes": True
    }


class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }