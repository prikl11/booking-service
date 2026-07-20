from fastapi import APIRouter, File, Form, UploadFile
from typing import Annotated

from app.database.schemas import (
    HotelImageResponse,
    HotelImageCreate,
)
from app.crud.hotel_images import (
    get_all_hotel_images,
    get_hotel_image_by_id,
    get_hotel_images_by_hotel_id,
    create_hotel_image,
    delete_hotel_image,
)
from app.utils.files import save_upload_file
from app.api.dependencies import SessionDep, CurrentUserDep
from app.crud.hotel_staff import check_hotel_role
from app.database.models.hotel_staff import Role
from app.utils.exceptions import ForbiddenException


router = APIRouter(prefix="/hotel-images", tags=["hotel-images"])


@router.get("/", response_model=list[HotelImageResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_hotel_images(db=db, skip=skip, limit=limit)
    return result


@router.get("/by-hotel/{hotel_id}", response_model=list[HotelImageResponse])
async def get_all_by_hotel(
    db: SessionDep,
    hotel_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_hotel_images_by_hotel_id(db=db, hotel_id=hotel_id, skip=skip, limit=limit)
    return result


@router.get("/{image_id}", response_model=HotelImageResponse)
async def get_by_id(db: SessionDep, image_id: int):
    result = await get_hotel_image_by_id(db=db, hotel_image_id=image_id)
    return result


@router.post("/", response_model=HotelImageResponse)
async def create(
    db: SessionDep,
    current_user: CurrentUserDep,
    hotel_id: Annotated[int, Form()],
    file: Annotated[UploadFile, File()],
):
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=hotel_id,
        roles=[Role.owner, Role.administrator,],
    )
    if check or current_user.is_admin:
        file_path = await save_upload_file(file=file, directory="hotels")
        result = await create_hotel_image(db=db, hotel_image=HotelImageCreate(hotel_id=hotel_id), image_url=file_path)
        return result
    else:
        raise ForbiddenException("No permission")


@router.delete("/{image_id}", response_model=HotelImageResponse)
async def delete(
    db: SessionDep, 
    image_id: int,
    current_user: CurrentUserDep,
    ):
    image = await get_hotel_image_by_id(db=db, hotel_image_id=image_id)
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=image.hotel_id,
        roles=[Role.owner, Role.administrator,],
    )
    if check or current_user.is_admin:
        result = await delete_hotel_image(db=db, hotel_image_id=image_id)
        return result
    else:
        raise ForbiddenException("No permission")
