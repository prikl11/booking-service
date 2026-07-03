from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import HotelService
from app.database.schemas import HotelServiceCreate
from app.utils.exceptions import NotFoundException, AlreadyExistsException


async def get_all_hotel_services(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelService]:
    """Return a paginated list of hotel services"""
    result = await db.execute(select(HotelService).offset(skip).limit(limit))
    return result.scalars().all()


async def get_hotel_services_by_hotel_id(
        db: AsyncSession,
        hotel_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelService]:
    """
    Return a paginated list of hotel services by hotel's ID
    """
    result = await db.execute(
        select(HotelService)
        .where(HotelService.hotel_id == hotel_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_hotel_services_by_service_id(
        db: AsyncSession,
        service_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[HotelService]:
    """
    Return a paginated list of hotel services by service ID
    """
    result = await db.execute(
        select(HotelService)
        .where(HotelService.service_id == service_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_hotel_services_by_hotel_and_service_ids(
        db: AsyncSession,
        hotel_id: int,
        service_id: int,
) -> HotelService:
    """
    Return a hotel service by hotel and service IDs
    """
    result = await db.execute(select(HotelService).where(
        HotelService.hotel_id == hotel_id,
        HotelService.service_id == service_id,
    ))
    if result.scalar_one_or_none() is None:
        raise NotFoundException("Hotel service not found")
    return result.scalar_one_or_none()


async def create_hotel_service(db: AsyncSession, hotel_service: HotelServiceCreate) -> HotelService:
    """Create and return a new hotel service"""
    existing = await db.execute(select(HotelService).where(
        HotelService.hotel_id == hotel_service.hotel_id,
        HotelService.service_id == hotel_service.service_id,
    ))
    if existing.scalar_one_or_none():
        raise AlreadyExistsException("Hotel service already exists")
    
    created = HotelService(**hotel_service.model_dump())

    db.add(created)
    await db.commit()
    await db.refresh(created)

    return created


async def delete_hotel_service(
        db: AsyncSession,
        hotel_id: int,
        service_id: int,
) -> HotelService:
    """
    Delete and return a hotel service by hotel and service IDs
    """
    existing = await get_hotel_services_by_hotel_and_service_ids(
        db=db,
        hotel_id=hotel_id,
        service_id=service_id,
    )

    db.delete(existing)
    await db.commit()

    return existing