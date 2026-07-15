from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select

from app.database.schemas import UserCreate, UserUpdate, UserResponse
from app.database.models import User
from app.utils.exceptions import AlreadyExistsException, NotFoundException
from app.utils.security import hash_password

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 20) -> Sequence[User]:
    """Return a paginated list of users"""
    results = await db.execute(select(User).offset(skip).limit(limit))
    return results.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Return a user by ID"""
    result = await db.get(User, user_id)
    if not result:
        raise NotFoundException("User not found")
    return result

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Return a user by email"""
    query = await db.execute(select(User).where(User.email == email))
    result = query.scalars().all()
    if result is None:
        raise NotFoundException("User not found")
    return query

async def get_user_by_phone(db: AsyncSession, phone: str) -> User | None:
    """Return a user by phone"""
    query = await db.execute(select(User).where(User.phone == phone))
    result = query.scalars().all()
    if result is None:
        raise NotFoundException("User not found")
    return query


async def set_admin(
        db: AsyncSession,
        user_id: int,
) -> User:
    user = await get_user_by_id(db=db, user_id=user_id)
    user.is_admin = True

    await db.commit()
    await db.refresh(user)

    return user


async def create_user(
        db: AsyncSession, 
        user: UserCreate,
        image_url: str | None = None,
        ) -> User:
    """Create and return a new user"""
    existing_user = await db.execute(select(User).where(
        User.email == user.email,
        User.phone == user.phone,
    ))
    if existing_user.scalar_one_or_none():
        raise AlreadyExistsException("User already exists")
    
    user_data = user.model_dump()
    user_data["hashed_password"] = hash_password(password=user_data.pop("password"))
    if image_url is not None:
        user_data["image_url"] = image_url
        
    created_user = User(**user_data)

    db.add(created_user)
    await db.commit()
    await db.refresh(created_user)

    return created_user

async def update_user(
        db: AsyncSession, 
        user_id: int, 
        user_update: UserUpdate,
        image_url: str | None = None,
        ) -> User:
    """Update and return user"""
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException("User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    if image_url is not None:
        update_data["image_url"] = image_url
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)

    return user

async def delete_user(db: AsyncSession, user_id: int) -> User:
    """Delete and return user"""
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException("User not found")

    response_data = UserResponse.model_validate(user)

    await db.delete(user)
    await db.commit()

    return response_data
