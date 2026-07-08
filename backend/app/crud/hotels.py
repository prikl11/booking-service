from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Hotel
from app.database.schemas import HotelCreate, HotelUpdate, HotelResponse
from app.utils.exceptions import AlreadyExistsException, NotFoundException


async def get_all_hotels(
        db: AsyncSession,
        country: str | None = None,
        city: str | None = None,
        address: str | None = None,
        zip_code: str | None = None,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Hotel]:
    """Return a paginated list of hotels with params"""
    query = select(Hotel)

    if country:
        query = query.where(Hotel.country == country)
    if city:
        query = query.where(Hotel.city == city)
    if address:
        query = query.where(Hotel.address == address)
    if zip_code:
        query = query.where(Hotel.zip_code == zip_code)
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_hotel_by_id(db: AsyncSession, hotel_id: int) -> Hotel | None:
    """Return a hotel by id or None if not found"""
    result = await db.get(Hotel, hotel_id)
    return result


async def get_hotel_by_zip(db: AsyncSession, zip_code: str) -> Hotel | None:
    """Return a hotel by zip or None if not found"""
    result = await db.execute(select(Hotel).where(Hotel.zip_code == zip_code))
    return result.scalar_one_or_none()


async def create_hotel(db: AsyncSession, hotel: HotelCreate) -> Hotel:
    """Create and return a new hotel"""
    existing_hotel = await db.execute(select(Hotel).where(
        Hotel.name == hotel.name,
        Hotel.country == hotel.country,
        Hotel.city == hotel.city,
        Hotel.address == hotel.address,
    ))
    if existing_hotel.scalar_one_or_none():
        raise AlreadyExistsException("Hotel already exists")
    
    created_hotel = Hotel(**hotel.model_dump())

    db.add(created_hotel)
    await db.commit()
    await db.refresh(created_hotel)

    return created_hotel


async def update_hotel(
        db: AsyncSession,
        hotel_id: int,
        hotel: HotelUpdate
) -> Hotel:
    """Update and return a hotel"""
    existing_hotel = await db.get(Hotel, hotel_id)
    if not existing_hotel:
        raise NotFoundException("Hotel not found")
    
    for key, value in hotel.model_dump(exclude_unset=True).items():
        setattr(existing_hotel, key, value)
    
    await db.commit()
    await db.refresh(existing_hotel)

    return existing_hotel


async def delete_hotel(db: AsyncSession, hotel_id: int) -> Hotel:
    """Delete and return a hotel"""
    existing_hotel = await db.get(Hotel, hotel_id)
    if not existing_hotel:
        raise NotFoundException("Hotel not found")

    response_data = HotelResponse.model_validate(existing_hotel)

    await db.delete(existing_hotel)
    await db.commit()

    return response_data
