from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.orm import selectinload
from decimal import Decimal

from app.database.models import Room, RoomBed
from app.database.models.room_beds import BedType
from app.database.schemas import RoomCreate, RoomUpdate, RoomResponse
from app.utils.exceptions import NotFoundException, AlreadyExistsException, NotAvailablseException


def apply_room_filters(query, filters: dict):
    """Return a query with filters"""
    if filters.get("price_min") is not None:
        query = query.where(Room.price >= filters.get("price_min"))
    if filters.get("price_max") is not None:
        query = query.where(Room.price <= filters.get("price_max"))
    if filters.get("personas_min") is not None:
        query = query.where(Room.personas >= filters.get("personas_min"))
    if filters.get("personas_max") is not None:
        query = query.where(Room.personas <= filters.get("personas_max"))
    if filters.get("discount") is True:
        query = query.where(Room.discount > 0)
    if filters.get("bed_type") is not None:
        query = query.join(RoomBed).where(RoomBed.bed_type == filters.get("bed_type")).distinct()

    sort_fields = {
        "name": Room.name,
        "price": Room.price,
        "personas": Room.personas,
    }

    if filters.get("sort_by") in sort_fields:
        field = sort_fields[filters.get("sort_by")]
        query = query.order_by(field.asc() if filters.get("order") == "asc" else field.desc())
    
    return query


async def get_all_rooms(
        db: AsyncSession,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
        personas_min: int | None = None,
        personas_max: int | None = None,
        discount: bool | None = None,
        bed_type: str | BedType = None,
        sort_by: str | None = None,
        order: str | None = None,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Room]:
    """Return a paginated list of all of rooms"""
    query = select(Room).options(selectinload(Room.hotel))
    query = apply_room_filters(query=query, filters={
        "price_min": price_min,
        "price_max": price_max,
        "personas_min": personas_min,
        "personas_max": personas_max,
        "discount": discount,
        "bed_type": bed_type,
        "sort_by": sort_by,
        "order": order,
    })
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_all_rooms_by_hotel(
        db: AsyncSession,
        hotel_id: int,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
        personas_min: int | None = None,
        personas_max: int | None = None,
        discount: bool | None = None,
        bed_type: str | BedType = None,
        sort_by: str | None = None,
        order: str | None = None,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Room]:
    """
    Return a paginated list of rooms by hotel with params
    """
    query = select(Room).where(Room.hotel_id == hotel_id).options(selectinload(Room.hotel))
    query = apply_room_filters(query=query, filters={
        "price_min": price_min,
        "price_max": price_max,
        "personas_min": personas_min,
        "personas_max": personas_max,
        "discount": discount,
        "bed_type": bed_type,
        "sort_by": sort_by,
        "order": order,
    })
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_room_by_id(db: AsyncSession, room_id: int) -> Room:
    """Return room by id or None if not found"""
    result = await db.execute(
        select(Room)
        .options(selectinload(Room.hotel))
        .where(Room.id == room_id)
    )
    room = result.scalar_one_or_none()
    if not room:
        raise NotFoundException("Room not found")
    return room


async def create_room(db: AsyncSession, room: RoomCreate) -> Room:
    """Create and return a room"""
    existing_room = await db.execute(select(Room).where(
        Room.name == room.name,
        Room.hotel_id == room.hotel_id,
    ))
    if existing_room.scalar_one_or_none():
        raise AlreadyExistsException("Room already exists")
    
    created_room = Room(**room.model_dump())

    db.add(created_room)
    await db.commit()
    await db.refresh(created_room, attribute_names=["hotel"])

    return created_room


async def update_rooms_quantity(db: AsyncSession, room_id: int, delta: int) -> Room:
    """Change the number of rooms"""
    room = await get_room_by_id(db=db, room_id=room_id)
    
    if room.quantity + delta < 0:
        raise NotAvailablseException("Number of rooms can not be negative")
    room.quantity += delta
    
    return room


async def update_room(
        db: AsyncSession,
        room_id: int,
        updated_room: RoomUpdate,
) -> Room:
    """Update and return a room"""
    existing_room = await get_room_by_id(db=db, room_id=room_id)
    
    for key, value in updated_room.model_dump(exclude_unset=True).items():
        setattr(existing_room, key, value)

    await db.commit()
    await db.refresh(existing_room, attribute_names=["hotel"])

    return existing_room


async def delete_room(db: AsyncSession, room_id: int) -> Room:
    """Delete and return a room"""
    existing_room = await get_room_by_id(db=db, room_id=room_id)

    response_data = RoomResponse.model_validate(existing_room)

    await db.delete(existing_room)
    await db.commit()

    return response_data
