from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.schemas import RoomBedCreate, RoomBedUpdate, RoomBedResponse
from app.database.models import Room, RoomBed
from app.utils.exceptions import NotFoundException, AlreadyExistsException


async def get_all_room_beds(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomBed]:
    """Return a paginated list of room beds"""
    result = await db.execute(select(RoomBed).offset(skip).limit(limit))
    return result.scalars().all()


async def get_room_beds_by_room_id(
        db: AsyncSession,
        room_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomBed]:
    """
    Return a paginated list of room beds by room's ID
    """
    result = await db.execute(
        select(RoomBed)
        .where(RoomBed.room_id == room_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_room_bed_by_id(db: AsyncSession, room_bed_id: int) -> RoomBed:
    """Return a room bed by ID or None if not found"""
    result = await db.execute(
        select(RoomBed)
        .options(selectinload(RoomBed.room).selectinload(Room.hotel))
        .where(RoomBed.id == room_bed_id)
    )
    room_bed = result.scalar_one_or_none()
    if not room_bed:
        raise NotFoundException("Room bed not found")
    return room_bed


async def create_room_bed(db: AsyncSession, room_bed: RoomBedCreate) -> RoomBed:
    """Create and return a new room bed"""
    existing = await db.execute(select(RoomBed).where(
        RoomBed.room_id == room_bed.room_id,
        RoomBed.bed_type == room_bed.bed_type
    ))
    if existing.scalar_one_or_none():
        raise AlreadyExistsException("Room bed already exists")
    
    created = RoomBed(**room_bed.model_dump())

    db.add(created)
    await db.commit()
    await db.refresh(created)

    return created


async def update_room_bed(
        db: AsyncSession,
        room_bed_id: int,
        updated_room_bed: RoomBedUpdate,
) -> RoomBed:
    """Update and return a room bed"""
    existing = await get_room_bed_by_id(db=db, room_bed_id=room_bed_id)

    for key, value in updated_room_bed.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


async def delete_room_bed(db: AsyncSession, room_bed_id: int) -> RoomBed:
    """Delete and return a room bed"""
    existing = await get_room_bed_by_id(db=db, room_bed_id=room_bed_id)

    response_data = RoomBedResponse.model_validate(existing)

    await db.delete(existing)
    await db.commit()

    return response_data
