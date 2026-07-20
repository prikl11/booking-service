from decimal import Decimal

from fastapi import APIRouter

from app.database.schemas import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
)
from app.crud.rooms import (
    get_all_rooms,
    get_all_rooms_by_hotel,
    get_room_by_id,
    create_room,
    update_room,
    delete_room,
)
from app.api.dependencies import SessionDep, CurrentUserDep
from app.database.models.room_beds import BedType
from app.database.models.hotel_staff import Role
from app.crud.hotel_staff import check_hotel_role
from app.utils.exceptions import ForbiddenException


router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/", response_model=list[RoomResponse])
async def get_all(
    db: SessionDep,
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
):
    result = await get_all_rooms(
        db=db,
        price_min=price_min,
        price_max=price_max,
        personas_min=personas_min,
        personas_max=personas_max,
        discount=discount,
        bed_type=bed_type,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-hotel/{hotel_id}", response_model=list[RoomResponse])
async def get_by_hotel(
    db: SessionDep,
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
):
    result = await get_all_rooms_by_hotel(
        db=db,
        price_min=price_min,
        price_max=price_max,
        personas_min=personas_min,
        personas_max=personas_max,
        discount=discount,
        bed_type=bed_type,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit,        
    )
    return result


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(db: SessionDep, room_id: int):
    result = await get_room_by_id(db=db, room_id=room_id)
    return result


@router.post("/", response_model=RoomResponse)
async def create(
    db: SessionDep, 
    room: RoomCreate,
    current_user: CurrentUserDep,
    ):
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator,],
    )
    if check or current_user.is_admin:
        result = await create_room(db=db, room=room)
        return result
    else:
        raise ForbiddenException("No permission")


@router.patch("/{room_id}", response_model=RoomResponse)
async def update(
    db: SessionDep,
    room_id: int,
    room: RoomUpdate,
    current_user: CurrentUserDep,
):
    room_in_db = await get_room_by_id(db=db, room_id=room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room_in_db.hotel_id,
        roles=[Role.owner, Role.administrator,],
    )
    if check or current_user.is_admin:
        result = await update_room(
            db=db,
            room_id=room_id,
            updated_room=room,
        )
        return result
    else:
        raise ForbiddenException("No permission")


@router.delete("/{room_id}", response_model=RoomResponse)
async def delete(
    db: SessionDep, 
    room_id: int,
    current_user: CurrentUserDep,
    ):
    room = await get_room_by_id(db=db, room_id=room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator,],
    )
    if check or current_user.is_admin:
        result = await delete_room(db=db, room_id=room_id)
        return result
    else:
        raise ForbiddenException("No permission")