from fastapi import APIRouter, File, UploadFile, Form
from typing import Annotated

from app.crud.services import (
    get_all_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service
)
from app.utils.files import save_upload_file
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
async def create(
    db: SessionDep,
    name: Annotated[str, Form()],
    file: Annotated[UploadFile, File()]
):
    file_path = await save_upload_file(file=file, directory="services")
    result = await create_service(db=db, service=ServiceCreate(name=name), image_url=file_path)
    return result


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update(
    db: SessionDep,
    service_id: int,
    name: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
):
    file_path = None
    if file is not None:
        file_path = await save_upload_file(file=file, directory="services")
    
    update_data = {}
    if name is not None:
        update_data["name"] = name

    result = await update_service(db=db, service_id=service_id, updated_service=ServiceUpdate(**update_data), image_url=file_path)
    return result


@router.delete("/{service_id}", response_model=ServiceResponse)
async def delete(db: SessionDep, service_id: int):
    result = await delete_service(db=db, service_id=service_id)
    return result