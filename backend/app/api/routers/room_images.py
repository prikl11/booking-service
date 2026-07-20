from fastapi import APIRouter, Form, File, UploadFile
from typing import Annotated

from app.database.schemas import RoomImageCreate, RoomImageResponse
from app.crud.room_images import (
    get_all_room_images,
    get_room_image_by_id,
    get_room_images_by_room_id,
    create_room_image,
    delete_room_image
)
from app.api.dependencies import SessionDep, CurrentUserDep
from app.utils.files import save_upload_file
from app.crud.rooms import get_room_by_id
from app.database.models.hotel_staff import Role
from app.crud.hotel_staff import check_hotel_role
from app.utils.exceptions import ForbiddenException


router = APIRouter(prefix="/room-images", tags=["room-images"])


@router.get("/", response_model=list[RoomImageResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_room_images(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-room/{room_id}", response_model=list[RoomImageResponse])
async def get_by_room(
    db: SessionDep,
    room_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_room_images_by_room_id(
        db=db,
        room_id=room_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/{image_id}", response_model=RoomImageResponse)
async def get_room_image(db: SessionDep, image_id: int):
    result = await get_room_image_by_id(db=db, room_image_id=image_id)
    return result


@router.post("/", response_model=RoomImageResponse)
async def create(
    db: SessionDep,
    current_user: CurrentUserDep,
    room_id: Annotated[int, Form()],
    image: Annotated[UploadFile, File()],
):
    room = await get_room_by_id(db=db, room_id=room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator,]
    )
    if check or current_user.is_admin:
        file_path = await save_upload_file(file=image, directory="rooms")
        result = await create_room_image(
            db=db,
            room_image=RoomImageCreate(room_id=room_id),
            image_url=file_path,
        )
        return result
    else:
        raise ForbiddenException("No permission")


@router.delete("/{image_id}", response_model=RoomImageResponse)
async def delete(
    db: SessionDep, 
    image_id: int,
    current_user: CurrentUserDep,
):
    image = await get_room_image_by_id(db=db, image_id=image_id)
    room = await get_room_by_id(db=db, room_id=image.room_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=room.hotel_id,
        roles=[Role.owner, Role.administrator,]
    )
    if check or current_user.is_admin:
        result = await delete_room_image(db=db, room_image_id=image_id)
        return result
    else:
        raise ForbiddenException("No permission")
