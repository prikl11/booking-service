from fastapi import APIRouter

from app.database.schemas import CartCreate, CartResponse
from app.crud.cart import (
    get_all_carts,
    get_all_carts_by_user_id,
    get_cart_by_id,
    get_active_cart_by_user_id,
    get_or_create_active_cart,
    checkout_cart,
    create_cart,
    delete_cart,
)
from app.api.dependencies import (
    SessionDep,
    AdminUserDep,
    CurrentUserDep,
)


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=list[CartResponse])
async def get_all(
    db: SessionDep,
    admin: AdminUserDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_carts(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-user/", response_model=list[CartResponse])
async def get_all_by_current_user(
    db: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_carts_by_user_id(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-user/{user_id}", response_model=list[CartResponse])
async def get_all_by_user(
    db: SessionDep,
    user_id: int,
    admin: AdminUserDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_carts_by_user_id(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/me", response_model=CartResponse)
async def get_my_cart(db: SessionDep, current_user: CurrentUserDep):
    result = await get_or_create_active_cart(db=db, user_id=current_user.id)
    return result


@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart(
    db: SessionDep,
    cart_id: int,
    admin: AdminUserDep,
):
    result = await get_cart_by_id(db=db, cart_id=cart_id)
    return result

@router.post("/checkout", response_model=CartResponse)
async def checkout(db: SessionDep, current_user: CurrentUserDep):
    active_cart = await get_active_cart_by_user_id(db=db, user_id=current_user.id)
    result = await checkout_cart(db=db, cart_id=active_cart.id)
    return result


@router.delete("/{cart_id}", response_model=CartResponse)
async def delete(
    db: SessionDep,
    cart_id: int,
    admin: AdminUserDep,
):
    result = await delete_cart(db=db, cart_id=cart_id)
    return result