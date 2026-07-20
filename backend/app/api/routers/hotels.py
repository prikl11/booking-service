from fastapi import APIRouter

from app.crud.hotels import (
    get_all_hotels,
    get_hotel_by_id,
    get_hotel_by_zip,
    create_hotel,
    update_hotel,
    delete_hotel,
)
from app.database.schemas import HotelResponse, HotelCreate, HotelUpdate
from app.api.dependencies import SessionDep, AdminUserDep, CurrentUserDep
from app.crud.hotel_staff import check_hotel_role
from app.utils.exceptions import ForbiddenException
from app.database.models.hotel_staff import Role


router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("/", response_model=list[HotelResponse])
async def get_all(
    db: SessionDep,
    country: str | None = None,
    city: str | None = None,
    address: str | None = None,
    zip_code: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_hotels(
        db=db,
        country=country,
        city=city,
        address=address,
        zip_code=zip_code,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-zip/{zip_code}", response_model=HotelResponse)
async def get_hotel_by_zip_code(db: SessionDep, zip_code: str):
    result = await get_hotel_by_zip(db=db, zip_code=zip_code)
    return result


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(db: SessionDep, hotel_id: int):
    result = await get_hotel_by_id(db=db, hotel_id=hotel_id)
    return result


@router.post("/", response_model=HotelResponse)
async def create(
    db: SessionDep, 
    hotel: HotelCreate,
    admin: AdminUserDep,
    ):
    result = await create_hotel(db=db, hotel=hotel)
    return result


@router.patch("/{hotel_id}", response_model=HotelResponse)
async def update(
    db: SessionDep,
    hotel_id: int,
    hotel: HotelUpdate,
    current_user: CurrentUserDep
):
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=hotel_id,
        roles=[Role.owner, Role.administrator,]
    )
    if check or current_user.is_admin:
        result = await update_hotel(db=db, hotel_id=hotel_id, hotel=hotel)
        return result
    else:
        raise ForbiddenException("No permission")


@router.delete("/{hotel_id}", response_model=HotelResponse)
async def delete(
    db: SessionDep, 
    hotel_id: int,
    current_user: CurrentUserDep,
    ):
    check = await check_hotel_role(
        db=db,
        user_id=current_user.id,
        hotel_id=hotel_id,
        roles=[Role.owner,],
    )
    if check or current_user.is_admin:
        result = await delete_hotel(db=db, hotel_id=hotel_id)
        return result
    else:
        raise ForbiddenException("No permission")