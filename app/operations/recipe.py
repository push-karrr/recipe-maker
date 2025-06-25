from datetime import datetime, timezone
from fastapi import HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.models import Recipe, Ingredient, Step
from app.schemas import CreateRecipe, UpdateRecipe
from app.database import get_session
from app.logger import logger


async def create_new_recipe(recipe:CreateRecipe, secure_id:int, session:AsyncSession = Depends(get_session)):
    new_recipe = Recipe(
        recipe_name=recipe.recipe_name,
        user_id=secure_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(new_recipe)
    await session.flush()


    ingredients = [
        Ingredient(
            name=ingredient.name,
            quantity=ingredient.quantity,
            recipe_id=new_recipe.id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        for ingredient in recipe.ingredients
    ]
    session.add_all(ingredients)

    steps = [
                Step(
                    step_name=step.step_name,
                    duration=step.duration,
                    recipe_id=new_recipe.id,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                ) for step in recipe.steps
            ]
    session.add_all(steps)

    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe

async def get_recipe_by_name(recipe_name:str, session:AsyncSession = Depends(get_session)) -> Recipe:
    result = await session.execute(
        select(Recipe)
        .where(func.lower(Recipe.recipe_name).ilike(f"%{recipe_name.lower()}%"))
        .options(
            selectinload(Recipe.ingredients),
            selectinload(Recipe.steps)
        )
    )
    recipe = result.scalar()
    if recipe is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe

async def get_recipe_by_id(recipe_id:int, session:AsyncSession = Depends(get_session)) -> Recipe:
    result = await session.execute(
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(
            selectinload(Recipe.ingredients),
            selectinload(Recipe.steps)
        )
    )
    recipe = result.scalar_one_or_none()
    if recipe is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe

async def update_recipe(recipe_data:UpdateRecipe, recipe_id:int ,user_id:int, session:AsyncSession = Depends(get_session)):
    logger.info(f"Updating recipe {recipe_id}, for user {user_id}")
    result = await session.execute(
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .where(Recipe.user_id == user_id)
        .options(selectinload(Recipe.ingredients), selectinload(Recipe.steps))
    )
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to edit this recipe")

    recipe.name = recipe_data.recipe_name
    recipe.updated_at = datetime.now(timezone.utc)

    existing_ing = {ing.id: ing for ing in recipe.ingredients}

    for ing_data in recipe_data.ingredients:
        if ing_data.id and ing_data.id in existing_ing:
            ing = existing_ing[ing_data.id]
            ing.name = ing_data.name
            ing.quantity = ing_data.quantity
            ing.updated_at = datetime.now(timezone.utc)
        else:
            new_ing = Ingredient(
                name=ing_data.name,
                quantity=ing_data.quantity,
                recipe_id=recipe.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(new_ing)


    existing_step = {step.id: step for step in recipe.steps}

    for step_data in recipe_data.steps:
            if step_data.id and step_data.id in existing_step:
                step = existing_step[step_data.id]
                step.quantity = step_data.quantity
                step.updated_at = datetime.now(timezone.utc)

            else:
                new_step = Step(
                    step_name=step_data.step_name,
                    duration=step_data.duration,
                    recipe_id=recipe.id,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                session.add(new_step)
    await session.commit()
    await session.refresh(recipe)
    return recipe

async def delete_recipe(recipe_id:int, user_id:int, session:AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .where(Recipe.user_id == user_id)
    )
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    await session.delete(recipe)
    await session.commit()
    await session.refresh(recipe)
    return recipe