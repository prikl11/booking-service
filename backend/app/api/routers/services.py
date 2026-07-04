from fastapi import APIRouter

from app.crud.services import (
    get_all_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service
)
from app.database.schemas import ServiceResponse, ServiceCreate, ServiceUpdate
from app.api.dependencies import SessionDep


router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[ServiceResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_services(db=db, skip=skip, limit=limit)
    return result


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(db: SessionDep, service_id: int):
    result = await get_service_by_id(db=db, service_id=service_id)
    return result


@router.post("/", response_model=ServiceResponse)
async def create(db: SessionDep, service: ServiceCreate):
    result = await create_service(db=db, service=service)
    return result


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update(
    db: SessionDep,
    service_id: int,
    service: ServiceUpdate,
):
    result = await update_service(db=db, service_id=service_id, updated_service=service)
    return result


@router.delete("/{service_id}", response_model=ServiceResponse)
async def delete(db: SessionDep, service_id: int):
    result = await delete_service(db=db, service_id=service_id)
    return result