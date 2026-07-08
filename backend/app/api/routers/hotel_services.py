from fastapi import APIRouter

from app.database.schemas import (
    HotelServiceCreate,
    HotelServiceResponse,
)
from app.crud.hotel_services import (
    get_all_hotel_services,
    get_hotel_services_by_hotel_and_service_ids,
    get_hotel_services_by_hotel_id,
    get_hotel_services_by_service_id,
    create_hotel_service,
    delete_hotel_service,
)
from app.api.dependencies import SessionDep


router = APIRouter(prefix="/hotel-services", tags=["hotel-services"])


@router.get("/", response_model=list[HotelServiceResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_hotel_services(db=db, skip=skip, limit=limit)
    return result


@router.get("/by-hotel/{hotel_id}", response_model=list[HotelServiceResponse])
async def get_all_by_hotel(
    db: SessionDep,
    hotel_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_hotel_services_by_hotel_id(
        db=db,
        hotel_id=hotel_id,
        skip=skip,
        limit=limit
    )
    return result


@router.get("/by-service/{service_id}", response_model=list[HotelServiceResponse])
async def get_all_by_service(
    db: SessionDep,
    service_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_hotel_services_by_service_id(
        db=db,
        service_id=service_id,
        skip=skip,
        limit=limit
    )
    return result


@router.get("/{hotel_id}/{service_id}", response_model=HotelServiceResponse)
async def get_hotel_service(
    db: SessionDep,
    hotel_id: int,
    service_id: int,
):
    result = await get_hotel_services_by_hotel_and_service_ids(
        db=db,
        hotel_id=hotel_id,
        service_id=service_id
    )
    return result


@router.post("/", response_model=HotelServiceResponse)
async def create(
    db: SessionDep,
    hotel_service: HotelServiceCreate,
):
    result = await create_hotel_service(db=db, hotel_service=hotel_service)
    return result


@router.delete("/{hotel_id}/{service_id}", response_model=HotelServiceResponse)
async def delete(
    db: SessionDep,
    hotel_id: int,
    service_id: int,
):
    result = await delete_hotel_service(
        db=db,
        hotel_id=hotel_id,
        service_id=service_id,
    )
    return result
