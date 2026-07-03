from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import HotelImage
from app.database.schemas import HotelImageCreate, HotelImageUpdate
from app.utils.exceptions import NotFoundException


async def get_all_hotel_images(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelImage]:
    """Return a paginated list of hotel images"""
    result = await db.execute(select(HotelImage).offset(skip).limit(limit))
    return result.scalars().all()


async def get_hotel_images_by_hotel_id(
        db: AsyncSession,
        hotel_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelImage]:
    """
    Return a paginated list of hotel images by hotel ID
    """
    result = await db.execute(
        select(HotelImage)
        .where(HotelImage.hotel_id == hotel_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_hotel_image_by_id(db: AsyncSession, hotel_image_id: int) -> HotelImage:
    """Return a hotel image by ID or None if not found"""
    result = await db.get(HotelImage, hotel_image_id)
    if not result:
        raise NotFoundException("Hotel image not found")
    return result


async def create_hotel_image(db: AsyncSession, hotel_image: HotelImageCreate) -> HotelImage:
    """Create and return a new hotel image"""
    created = HotelImage(**hotel_image.model_dump())

    db.add(created)
    await db.commit()
    await db.refresh(created)

    return created


async def update_hotel_image(
        db: AsyncSession,
        hotel_image_id: int,
        updated_hotel_image: HotelImageUpdate,
) -> HotelImage:
    """Update and return a hotel image"""
    existing = await get_hotel_image_by_id(db=db, hotel_image_id=hotel_image_id)

    for key, value in updated_hotel_image.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


async def delete_hotel_image(db: AsyncSession, hotel_image_id: int) -> HotelImage:
    """Delete and return a hotel image"""
    existing = await get_hotel_image_by_id(db=db, hotel_image_id=hotel_image_id)

    db.delete(existing)
    await db.commit()

    return existing