from fastapi import APIRouter

from app.api.dependencies import SessionDep
from app.database.schemas import (
    HotelStaffCreate,
    HotelStaffResponse,
    HotelStaffUpdate,
)
from app.crud.hotel_staff import (
    get_all_hotell_staff,
    get_hotel_staff_by_hotel_id,
    get_hotel_staff_by_user_and_hotel_ids,
    get_hotel_staff_by_user_id,
    create_hotel_staff,
    update_hotel_staff,
    delete_hotel_staff,
)


router = APIRouter(prefix="/hotel-staff", tags=["hotel-staff"])


@router.get("/", response_model=list[HotelStaffResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_hotell_staff(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-user/{user_id}", response_model=list[HotelStaffResponse])
async def get_staff_by_user(
    db: SessionDep,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_hotel_staff_by_user_id(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-hotel/{hotel_id}", response_model=list[HotelStaffResponse])
async def get_staff_by_hotel(
    db: SessionDep,
    hotel_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_hotel_staff_by_hotel_id(
        db=db,
        hotel_id=hotel_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/{user_id}/{hotel_id}", response_model=HotelStaffResponse)
async def get_hotel_staff(
    db: SessionDep,
    user_id: int,
    hotel_id: int,
):
    result = await get_hotel_staff_by_user_and_hotel_ids(
        db=db,
        user_id=user_id,
        hotel_id=hotel_id,
    )
    return result


@router.post("/", response_model=HotelStaffResponse)
async def create(db: SessionDep, staff: HotelStaffCreate):
    result = await create_hotel_staff(db=db, hotel_staff=staff)
    return result


@router.patch("/{user_id}/{hotel_id}", response_model=HotelStaffResponse)
async def update(
    db: SessionDep,
    user_id: int,
    hotel_id: int,
    staff: HotelStaffUpdate,
):
    result = await update_hotel_staff(
        db=db,
        user_id=user_id,
        hotel_id=hotel_id,
        updated_hotel_staff=staff,
    )
    return result


@router.delete("/{user_id}/{hotel_id}", response_model=HotelStaffResponse)
async def delete(
    db: SessionDep,
    user_id: int,
    hotel_id: int,
):
    result = await delete_hotel_staff(
        db=db,
        user_id=user_id,
        hotel_id=hotel_id,
    )
    return result