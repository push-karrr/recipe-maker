from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database import get_session
from app.operations.users import create_user, login_user
from app.logger import logger
from app.utils import create_access_token

router = APIRouter(prefix="/users/v1", tags=["users"])

@router.post("/create", response_model=schemas.UserResponse)
async def create_user_(
        user: schemas.UserCreate,
        session: AsyncSession = Depends(get_session),
):
    return await create_user(name=user.name, email=user.email, password=user.password, session=session)


@router.post("/login")
async def login(
        username: str,
        password: str,
        session: AsyncSession = Depends(get_session)
):
    user = await login_user(name=username, password=password, session=session)
    if not user:
        logger.info(f"User {username} not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    logger.info(f"User {username} logged in successfully.")
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(hours=0.5))
    return {"access_token": access_token, "token_type": "bearer"}

