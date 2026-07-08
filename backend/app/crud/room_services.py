from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.orm import selectinload

from app.database.models import Room, RoomService
from app.database.schemas import RoomServiceCreate, RoomServiceResponse
from app.utils.exceptions import NotAvailablseException, NotFoundException, AlreadyExistsException


async def get_all_room_services(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomService]:
    """Return a paginates list of room services"""
    result = await db.execute(select(RoomService).offset(skip).limit(limit))
    return result.scalars().all()


async def get_room_services_by_room_id(
        db: AsyncSession,
        room_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomService]:
    """
    Return a paginated list of room services by room's ID
    """
    result = await db.execute(
        select(RoomService)
        .where(RoomService.room_id == room_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_room_services_by_service_id(
        db: AsyncSession,
        service_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomService]:
    """
    Return a paginated list of room services by service's ID
    """
    result = await db.execute(
        select(RoomService)
        .where(RoomService.service_id == service_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_room_service_by_service_and_room_ids(
        db: AsyncSession,
        room_id: int,
        service_id: int,
) -> RoomService:
    """
    Return a room service by room and service IDs or None if not found
    """
    result = await db.execute(
        select(RoomService)
        .options(
            selectinload(RoomService.room).selectinload(Room.hotel),
            selectinload(RoomService.service),
        )
        .where(
            RoomService.room_id == room_id,
            RoomService.service_id == service_id,
        )
    )
    room_service = result.scalar_one_or_none()
    if room_service is None:
        raise NotFoundException("Room service not found")
    return room_service


async def create_room_service(db: AsyncSession, room_service: RoomServiceCreate) -> RoomService:
    """Create and return a new room service"""
    existing = await db.execute(select(RoomService).where(
        RoomService.room_id == room_service.room_id,
        RoomService.service_id == room_service.service_id,
    ))
    if existing.scalar_one_or_none():
        raise AlreadyExistsException("Room service already exists")
    
    created = RoomService(**room_service.model_dump())

    db.add(created)
    await db.commit()
    await db.refresh(created)

    return created


async def delete_room_service(
        db: AsyncSession,
        room_id: int,
        service_id: int,
) -> RoomService:
    """Delete and return a room service"""
    existing = await get_room_service_by_service_and_room_ids(
        db=db, 
        room_id=room_id, 
        service_id=service_id
        )
    
    response_data = RoomServiceResponse.model_validate(existing)

    await db.delete(existing)
    await db.commit()

    return response_data
