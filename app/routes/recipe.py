from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import RecipeResponse, CreateRecipe, RecipeBase, UpdateRecipe

from app import schemas
from app.operations.recipe import create_new_recipe, get_recipe_by_name, get_recipe_by_id, update_recipe, delete_recipe
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/recipe/v1", tags=["Recipe"])

@router.post("/create", response_model=RecipeBase, status_code=status.HTTP_201_CREATED)
async def create_recipe(
        recipe: CreateRecipe,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
    ):

    return await create_new_recipe(session=session, recipe=recipe, secure_id=current_user.id)

@router.get("/get_recipe/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
async def get_recipe_id(recipe_id: int, session: AsyncSession = Depends(get_session)):
    return await get_recipe_by_id(session=session, recipe_id=recipe_id)

@router.get("/get_recipe/{name}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
async def get_recipe_name(recipe_name: str, session: AsyncSession = Depends(get_session)):
    return await get_recipe_by_name(session=session, recipe_name=recipe_name)
@router.patch("/update/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
async def update_recipe_end(
        recipe_id: int,
        recipe: UpdateRecipe,
        current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    return await update_recipe(recipe_data=recipe, recipe_id=recipe_id, user_id=current_user.id, session=session)

@router.delete("/delete/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe_end(recipe_id: int, session: AsyncSession = Depends(get_session),current_user = Depends(get_current_user)):
    return await delete_recipe(recipe_id=recipe_id, user_id = current_user.id, session=session)