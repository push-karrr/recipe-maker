from fastapi import HTTPException, status, Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.models import Users
from app.logger import logger
from app.utils import hash_password, verify_password


async def create_user(
    name: str,
    email: str,
    password: str,
    session: AsyncSession,
) -> Users:
    # Duplicate check
    if await session.scalar(select(Users).where(Users.name == name)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User '{name}' already exists.",
        )

    try:
        user = Users(
            name=name,
            email=email,
            password=hash_password(password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this e-mail already exists.",
        )
    except Exception as e:
        await session.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected database error.",
        )

async def login_user(name: str, password: str, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Users).where(Users.name == name))
        user = result.scalars().first()
        if user and verify_password(password, user.password):
            logger.info(f"User '{name}' authenticated")
            return user
        logger.warning(f"Invalid login attempt for user '{name}'")
        return None
    except Exception as e:
        logger.error(f"Login failed. Error: {e}")
        raise