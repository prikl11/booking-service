from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import (
    SessionDep,
    CurrentUserDep,
    AdminUserDep,
)
from app.api.forms import UserUpdateFormData
from app.utils.files import save_upload_file
from app.database.schemas import (
    UserResponse,
    UserUpdate,
)
from app.crud.users import (
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    get_user_by_phone,
    set_admin,
    update_user,
    delete_user,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_users(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.get("/by-email/{email}", response_model=UserResponse)
async def get_by_email(db: SessionDep, email: str):
    result = await get_user_by_email(db=db, email=email)
    return result


@router.get("/by-phone/{phone}", response_model=UserResponse)
async def get_by_phone(db: SessionDep, phone: str):
    result = await get_user_by_phone(db=db, phone=phone)
    return result


@router.get("/{user_id}", response_model=UserResponse)
async def get_by_id(db: SessionDep, user_id: int):
    result = await get_user_by_id(db=db, user_id=user_id)
    return result


@router.post("/admin/{user_id}", response_model=UserResponse)
async def set_user_admin(
    db: SessionDep,
    admin: AdminUserDep,
    user_id: int,
):
    result = await set_admin(db=db, user_id=user_id)
    return result


@router.patch("/{user_id}", response_model=UserResponse)
async def update(
    db: SessionDep,
    user_id: int,
    form: Annotated[UserUpdateFormData, Depends()],
    image: Annotated[UploadFile | None, File()] = None,
):
    image_url = None
    if image is not None:
        image_url = await save_upload_file(file=image, directory="users")

    update_data = {k: v for k, v in form.to_dict().items() if v is not None}

    result = await update_user(
        db=db,
        user_id=user_id,
        user_update=UserUpdate(**update_data),
        image_url=image_url
    )
    return result


@router.delete("/{user_id}", response_model=UserResponse)
async def delete(db: SessionDep, user_id: int):
    result = await delete_user(db=db, user_id=user_id)
    return result