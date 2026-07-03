from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import HotelStaff
from app.database.schemas import HotelStaffCreate, HotelStaffUpdate
from app.utils.exceptions import NotFoundException, AlreadyExistsException


async def get_all_hotell_staff(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelStaff]:
    """Return a paginated list of hotel staff"""
    result = await db.execute(select(HotelStaff).offset(skip).limit(limit))
    return result.scalars().all()


async def get_hotel_staff_by_user_id(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelStaff]:
    """Return a paginated list of hotel staff by user ID"""
    result = await db.execute(
        select(HotelStaff)
        .where(HotelStaff.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_hotel_staff_by_hotel_id(
        db: AsyncSession,
        hotel_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelStaff]:
    """Return a paginated list of hotel staff by hotel ID"""
    result = await db.execute(
        select(HotelStaff)
        .where(HotelStaff.hotel_id == hotel_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_hotel_staff_by_user_and_hotel_ids(
        db: AsyncSession,
        user_id: int,
        hotel_id: int,
) -> HotelStaff:
    """
    Return a hotel staff by user's and hotel's IDs
    """
    result = await db.execute(select(HotelStaff).where(
        HotelStaff.user_id == user_id,
        HotelStaff.hotel_id == hotel_id,
    ))
    if result.scalar_one_or_none() is None:
        raise NotFoundException("Hotel staff not found")
    return result.scalar_one_or_none()


async def create_hotel_staff(db: AsyncSession, hotel_staff: HotelStaffCreate) -> HotelStaff:
    """Create and return a new hotel staff"""
    existing = await db.execute(select(HotelStaff).where(
        HotelStaff.user_id == hotel_staff.user_id,
        HotelStaff.hotel_id == hotel_staff.hotel_id,
    ))
    if existing.scalar_one_or_none():
        raise AlreadyExistsException("Hotel staff already exists")
    
    created = HotelStaff(**hotel_staff.model_dump())

    db.add(created)
    await db.commit()
    await db.refresh(created)

    return created


async def update_hotel_staff(
        db: AsyncSession,
        user_id: int,
        hotel_id: int,
        updated_hotel_staff: HotelStaffUpdate,
) -> HotelStaff:
    """Update and return a hotel staff"""
    existing = await get_hotel_staff_by_user_and_hotel_ids(
        db=db,
        user_id=user_id,
        hotel_id=hotel_id,
    )

    for key, value in updated_hotel_staff.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


async def delete_hotel_staff(
        db: AsyncSession,
        user_id: int,
        hotel_id: int,
) -> HotelStaff:
    """Delete and return a hotel staff"""
    existing = await get_hotel_staff_by_user_and_hotel_ids(
        db=db,
        user_id=user_id,
        hotel_id=hotel_id,
    )

    db.delete(existing)
    await db.commit()

    return existing