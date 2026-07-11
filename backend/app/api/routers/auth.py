from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.utils.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_refresh_token,
)
from app.database.schemas import UserCreate, TokenResponse
from app.api.dependencies import SessionDep
from app.crud.users import (
    get_user_by_email,
    get_user_by_id,
    create_user
)
from app.utils.files import save_upload_file
from app.api.forms import UserFormData


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    db: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    expires_delta: timedelta | None = None,
):
    user = await get_user_by_email(db=db, email=form_data.username)
    if user is None or not verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=expires_delta)
    refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=expires_delta)

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    db: SessionDep, 
    refresh_token: str,
    expires_delta: timedelta | None = None,
    ):
    payload = decode_refresh_token(token=refresh_token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = await get_user_by_id(db=db, user_id=int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=expires_delta)
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=expires_delta)

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=TokenResponse)
async def register(
    db: SessionDep, 
    form: Annotated[UserFormData, Depends()],
    image: Annotated[UploadFile | None, File()] = None,
    ):
    image_url = None
    if image is not None:
        image_url = await save_upload_file(file=image, directory="users")

    user = await create_user(
        db=db, 
        user=UserCreate(**form.to_dict()),
        image_url=image_url
    )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }