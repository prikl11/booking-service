from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Room, RoomImage
from app.database.schemas import RoomImageCreate, RoomImageUpdate, RoomImageResponse
from app.utils.exceptions import NotAvailablseException, NotFoundException, AlreadyExistsException


async def get_all_room_images(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomImage]:
    """Return a paginated list of all room images"""
    result = await db.execute(select(RoomImage).offset(skip).limit(limit))
    return result.scalars().all()


async def get_room_images_by_room_id(
        db: AsyncSession,
        room_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomImage]:
    """
    Return a paginated list of all room images by room's ID
    """
    result = await db.execute(select(RoomImage)
                              .where(RoomImage.room_id == room_id)
                              .offset(skip)
                              .limit(limit)
                              )
    return result.scalars().all()


async def get_room_image_by_id(db: AsyncSession, room_image_id: int) -> RoomImage:
    """
    Return a room's image by ID or None if not found
    """
    result = await db.execute(
        select(RoomImage)
        .options(selectinload(RoomImage.room).selectinload(Room.hotel))
        .where(RoomImage.id == room_image_id)
    )
    room_image = result.scalar_one_or_none()
    if not room_image:
        raise NotFoundException("Room image not found")
    return room_image


async def create_room_image(db: AsyncSession, room_image: RoomImageCreate) -> RoomImage:
    """Create and return a new room image"""
    created = RoomImage(**room_image.model_dump())

    db.add(created)
    await db.commit()
    await db.refresh(created)

    return created


async def update_room_image(
        db: AsyncSession,
        room_image_id: int,
        updated_room_image: RoomImageUpdate,
) -> RoomImage:
    """Update and return a room image"""
    existing = await get_room_image_by_id(db=db, room_image_id=room_image_id)

    for key, value in updated_room_image.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


async def delete_room_image(db: AsyncSession, room_image_id: int) -> RoomImage:
    """Delete and return a room image"""
    existing = await get_room_image_by_id(db=db, room_image_id=room_image_id)

    response_data = RoomImageResponse.model_validate(existing)

    await db.delete(existing)
    await db.commit()

    return response_data
