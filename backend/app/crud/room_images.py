from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Room, RoomImage
from app.database.schemas import RoomImageCreate, RoomImageResponse
from app.utils.exceptions import NotFoundException


async def get_all_room_images(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[RoomImage]:
    """Return a paginated list of all room images"""
    result = await db.execute(
        select(RoomImage)
        .options(selectinload(RoomImage.room).selectinload(Room.hotel))
        .offset(skip)
        .limit(limit)
    )
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
                              .options(selectinload(RoomImage.room).selectinload(Room.hotel))
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


async def create_room_image(
        db: AsyncSession,
        room_image: RoomImageCreate,
        image_url: str,
) -> RoomImage:
    """Create and return a new room image"""
    created = RoomImage(**room_image.model_dump(), image_url=image_url)

    image_id = created.id
    room_id = created.room_id

    db.add(created)
    await db.commit()
    result = await db.execute(
        select(RoomImage)
        .options(selectinload(RoomImage.room).selectinload(Room.hotel))
        .where(
            RoomImage.id == image_id,
            RoomImage.room_id == room_id,
            )
    )

    return result.scalar_one()


async def delete_room_image(db: AsyncSession, room_image_id: int) -> RoomImage:
    """Delete and return a room image"""
    existing = await get_room_image_by_id(db=db, room_image_id=room_image_id)

    response_data = RoomImageResponse.model_validate(existing)

    await db.delete(existing)
    await db.commit()

    return response_data
