from fastapi import APIRouter

from app.database.schemas import (
    RoomBedCreate,
    RoomBedUpdate,
    RoomBedResponse,
)
from app.crud.room_beds import (
    get_all_room_beds,
    get_room_bed_by_id,
    get_room_beds_by_room_id,
    create_room_bed,
    update_room_bed,
    delete_room_bed,
)
from app.api.dependencies import SessionDep, CurrentUserDep
from app.crud.hotel_staff import check_hotel_role
from app.crud.rooms import get_room_by_id
from app.database.models.hotel_staff import Role
from app.utils.exceptions import ForbiddenException



router = APIRouter(prefix="/room-beds", tags=["room-beds"])


@router.get("/", response_model=list[RoomBedResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_room_beds(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-room/{room_id}", response_model=list[RoomBedResponse])
async def get_by_room(
    db: SessionDep,
    room_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_room_beds_by_room_id(
        db=db,
        room_id=room_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/{bed_id}", response_model=RoomBedResponse)
async def get_room_bed(db: SessionDep, bed_id: int):
    result = await get_room_bed_by_id(db=db, room_bed_id=bed_id)
    return result


@router.post("/", response_model=RoomBedResponse)
async def create(
    db: SessionDep, 
    room_bed: RoomBedCreate,
    current_user: CurrentUserDep,
    ):
    room = await get_room_by_id(db=db, room_id=room_bed.room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator],
    )
    if check or current_user.is_admin:
        result = await create_room_bed(db=db, room_bed=room_bed)
        return result
    else:
        raise ForbiddenException("No permission")


@router.patch("/{bed_id}", response_model=RoomBedResponse)
async def update(
    db: SessionDep,
    bed_id: int,
    room_bed: RoomBedUpdate,
    current_user: CurrentUserDep,
):
    existing_bed = await get_room_bed_by_id(db=db, room_bed_id=bed_id)
    room = await get_room_by_id(db=db, room_id=existing_bed.room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator],
    )
    if check or current_user.is_admin:
        result = await update_room_bed(
            db=db,
            room_bed_id=bed_id,
            updated_room_bed=room_bed,
        )
        return result
    else:
        raise ForbiddenException("No permission")


@router.delete("/{bed_id}", response_model=RoomBedResponse)
async def delete(
    db: SessionDep, 
    bed_id: int,
    current_user: CurrentUserDep,
    ):
    room_bed = await get_room_bed_by_id(db=db, room_bed_id=bed_id)
    room = await get_room_by_id(db=db, room_id=room_bed.room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator],
    )
    if check or current_user.is_admin:
        result = await delete_room_bed(db=db, room_bed_id=bed_id)
        return result
    else:
        raise ForbiddenException("No permission")