from fastapi import APIRouter, HTTPException, status

from app.database.schemas import (
    BookingCreate,
    BookingResponse,
    BookingUpdate,
)
from app.crud.bookings import (
    get_all_bookings,
    get_all_bookings_by_cart,
    get_all_bookings_by_room,
    get_bookings_by_user_and_cart_ids,
    get_booking_by_id,
    create_booking,
    update_booking,
    delete_booking,
)
from app.crud.cart import get_or_create_active_cart
from app.crud.hotel_staff import is_hotel_staff
from app.crud.rooms import get_room_by_id
from app.api.dependencies import (
    SessionDep,
    CurrentUserDep,
    AdminUserDep,
)


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=list[BookingResponse])
async def get_all(
    db: SessionDep,
    admin: AdminUserDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_bookings(
        db=db,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-cart/me/active", response_model=list[BookingResponse])
async def get_bookings_in_active_cart(
    db: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 20,
):
    cart = await get_or_create_active_cart(db=db, user_id=current_user.id)
    result = await get_all_bookings_by_cart(
        db=db,
        cart_id=cart.id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-cart/me/{cart_id}", response_model=list[BookingResponse])
async def get_bookings_in_current_user_cart(
    db: SessionDep,
    current_user: CurrentUserDep,
    cart_id: int,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_bookings_by_user_and_cart_ids(
        db=db,
        user_id=current_user.id,
        cart_id=cart_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-cart/{cart_id}", response_model=list[BookingResponse])
async def get_bookings_by_cart(
    db: SessionDep,
    cart_id: int,
    admin: AdminUserDep,
    skip: int = 0,
    limit: int = 20,
):
    result = await get_all_bookings_by_cart(
        db=db,
        cart_id=cart_id,
        skip=skip,
        limit=limit,
    )
    return result


@router.get("/by-room/{room_id}", response_model=list[BookingResponse])
async def get_bookings_by_room(
    db: SessionDep,
    room_id: int,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 20,
):
   room = await get_room_by_id(db=db, room_id=room_id)

   if not (
       await is_hotel_staff(
           db=db,
           hotel_id=room.hotel_id,
           user_id=current_user.id,
       )
       or current_user.is_admin
   ):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
   
   result = await get_all_bookings_by_room(
       db=db,
       room_id=room_id,
       skip=skip,
       limit=limit,
   )
   return result


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    db: SessionDep, 
    booking_id: int,
    current_user: CurrentUserDep,
    ):
    result = await get_booking_by_id(db=db, booking_id=booking_id)
    if result.cart.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    return result


@router.post("/", response_model=BookingResponse)
async def create(
    db: SessionDep, 
    booking: BookingCreate,
    current_user: CurrentUserDep,
    ):
    result = await create_booking(
        db=db, 
        booking=booking,
        user_id=current_user.id,
        )
    return result


@router.patch("/{booking_id}", response_model=BookingResponse)
async def update(
    db: SessionDep,
    booking_id: int,
    booking: BookingUpdate,
    current_user: CurrentUserDep,
):
    existing = await get_booking_by_id(
        db=db, 
        booking_id=booking_id,
        )
    if existing.cart.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    result = await update_booking(
        db=db,
        booking_id=booking_id,
        updated_booking=booking,
    )
    return result


@router.delete("/{booking_id}", response_model=BookingResponse)
async def delete(
    db: SessionDep, 
    booking_id: int,
    current_user: CurrentUserDep,
    ):
    existing = await get_booking_by_id(db=db, booking_id=booking_id)
    if existing.cart.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    result = await delete_booking(db=db, booking_id=booking_id)
    return result