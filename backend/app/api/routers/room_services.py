from fastapi import APIRouter

from app.database.schemas import RoomServiceCreate, RoomServiceResponse
from app.crud.room_services import (
    get_all_room_services,
    get_room_service_by_service_and_room_ids,
    get_room_services_by_room_id,
    get_room_services_by_service_id,
    create_room_service,
    delete_room_service,
)
from app.api.dependencies import SessionDep, CurrentUserDep
from app.crud.hotel_staff import check_hotel_role
from app.crud.rooms import get_room_by_id
from app.database.models.hotel_staff import Role
from app.utils.exceptions import ForbiddenException


router = APIRouter(prefix="/room-services", tags=["room-services"])


@router.get("/", response_model=list[RoomServiceResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_room_services(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-room/{room_id}", response_model=list[RoomServiceResponse])
async def get_by_room(
    db: SessionDep,
    room_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_room_services_by_room_id(
        db=db,
        room_id=room_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-service/{service_id}", response_model=list[RoomServiceResponse])
async def get_by_service(
    db: SessionDep,
    service_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_room_services_by_service_id(
        db=db,
        service_id=service_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/{room_id}/{service_id}", response_model=RoomServiceResponse)
async def get_room_service(
    db: SessionDep,
    room_id: int,
    service_id: int,
):
    result = await get_room_service_by_service_and_room_ids(
        db=db,
        room_id=room_id,
        service_id=service_id,
    )
    return result


@router.post("/", response_model=RoomServiceResponse)
async def create(
    db: SessionDep, 
    room_service: RoomServiceCreate,
    current_user: CurrentUserDep,
    ):
    room = await get_room_by_id(db=db, room_id=room_service.room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator],
    )
    if check or current_user.is_admin:
        result = await create_room_service(db=db, room_service=room_service)
        return result
    else:
        raise ForbiddenException("No permission")


@router.delete("/{room_id}/{service_id}", response_model=RoomServiceResponse)
async def delete(
    db: SessionDep,
    room_id: int,
    service_id: int,
    current_user: CurrentUserDep,
):
    room = await get_room_by_id(db=db, room_id=room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator],
    )
    if check or current_user.is_admin:
        result = await delete_room_service(
            db=db,
            room_id=room_id,
            service_id=service_id,
        )
        return result
    else:
        raise ForbiddenException("No permission")