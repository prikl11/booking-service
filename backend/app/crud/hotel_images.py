from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import HotelImage
from app.database.schemas import HotelImageCreate, HotelImageResponse
from app.utils.exceptions import NotFoundException


async def get_all_hotel_images(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelImage]:
    """Return a paginated list of hotel images"""
    result = await db.execute(
        select(HotelImage)
        .options(selectinload(HotelImage.hotel))
        .offset(skip)
        .limit(limit)
    )
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
        .options(selectinload(HotelImage.hotel))
        .where(HotelImage.hotel_id == hotel_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_hotel_image_by_id(db: AsyncSession, hotel_image_id: int) -> HotelImage:
    """Return a hotel image by ID or None if not found"""
    result = await db.execute(
        select(HotelImage)
        .options(selectinload(HotelImage.hotel))
        .where(HotelImage.id == hotel_image_id)
    )
    image = result.scalar_one_or_none()
    if image is None:
        raise NotFoundException("Hotel image not found")
    return image


async def create_hotel_image(
        db: AsyncSession,
        hotel_image: HotelImageCreate,
        image_url: str,
) -> HotelImage:
    """Create and return a new hotel image"""
    created = HotelImage(**hotel_image.model_dump(), image_url=image_url)

    db.add(created)
    await db.commit()
    await db.refresh(created, attribute_names=["hotel"])

    return created


async def delete_hotel_image(db: AsyncSession, hotel_image_id: int) -> HotelImage:
    """Delete and return a hotel image"""
    existing = await get_hotel_image_by_id(db=db, hotel_image_id=hotel_image_id)

    response_data = HotelImageResponse.model_validate(existing)

    await db.delete(existing)
    await db.commit()

    return response_data