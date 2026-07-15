from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, Sequence, not_
from sqlalchemy.orm import selectinload

from app.database.models import Booking, Cart, Room
from app.database.schemas import BookingCreate, BookingUpdate, BookingResponse
from app.crud.rooms import get_room_by_id, update_rooms_quantity
from app.crud.cart import get_or_create_active_cart, get_active_cart_by_user_id
from app.utils.exceptions import NotFoundException, NotAvailablseException, AlreadyExistsException


async def get_all_bookings(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Booking]:
    """Return a paginated list of bookings by all of users"""
    result = await db.execute(
        select(Booking)
        .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
        .offset(skip)
        .limit(limit))
    return result.scalars().all()


async def get_all_bookings_by_cart(
        db: AsyncSession,
        cart_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Booking]:
    """Return a paginated list of bookings by cart's ID"""
    result = await db.execute(
            select(Booking)
            .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
            .where(Booking.cart_id == cart_id)
            .offset(skip)
            .limit(limit)
    )
    return result.scalars().all()


async def get_all_bookings_by_room(
        db: AsyncSession,
        room_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Booking]:
    """Return a paginated list of bookings by room's ID"""
    result = await db.execute(
        select(Booking)
        .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
        .where(Booking.room_id == room_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_bookings_by_user_and_cart_ids(
        db: AsyncSession,
        user_id: int,
        cart_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Booking:
    result = await db.execute(
        select(Booking)
        .join(Cart)
        .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
        .where(
            Booking.cart_id == cart_id,
            Cart.user_id == user_id
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_booking_by_id_and_user_id(
        db: AsyncSession,
        booking_id: int,
        user_id: int,
) -> Booking:
    query = await db.execute(
        select(Booking)
        .join(Cart)
        .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
        .where(
            Booking.id == booking_id,
            Cart.user_id == user_id,
        )
    )
    result = query.scalar_one_or_none()
    if result is None:
        raise NotFoundException("Booking not found")
    return result


async def get_booking_by_id(db: AsyncSession, booking_id: int) -> Booking:
    """Return a booking by its ID"""
    result = await db.execute(
        select(Booking)
        .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
        .where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise NotFoundException("Booking not found")
    return booking


async def create_booking(
        db: AsyncSession, 
        booking: BookingCreate,
        user_id: int,
        ) -> Booking:
    """
    Create booking, calc the total price and update the number of rooms
    """
    existing = await db.execute(select(Booking).where(
        Booking.room_id == booking.room_id
        ).where(
            not_(or_(
                Booking.departure_date <= booking.arrival_date,
                Booking.arrival_date >= booking.departure_date,
            ))
        ))
    if existing.scalar_one_or_none():
        raise AlreadyExistsException("Booking already exists")
    
    cart = await get_or_create_active_cart(db=db, user_id=user_id)
    room = await get_room_by_id(db=db, room_id=booking.room_id)

    if booking.people_quantity > room.personas:
        raise NotAvailablseException(f"The number of people must be less than {room.personas}")
    
    booking_data = booking.model_dump()
    
    booking_data["cart_id"] = cart.id

    if room.discount:
        booking_data["total_price"] = room.price * (1 - room.discount)
    else:
        booking_data["total_price"] = room.price
    
    created_booking = Booking(**booking_data)

    db.add(created_booking)
    await update_rooms_quantity(db=db, room_id=room.id, delta=-1)
    await db.commit()
    await db.refresh(created_booking)
    
    result = await db.execute(
        select(Booking)
        .options(
            selectinload(Booking.cart).selectinload(Cart.user),
            selectinload(Booking.room).selectinload(Room.hotel),
        )
        .where(Booking.id == created_booking.id)
    )

    return result.scalar_one()


async def update_booking(
        db: AsyncSession,
        booking_id: int,
        updated_booking: BookingUpdate,
) -> Booking:
    """Update and return a booking"""
    existing = await get_booking_by_id(db=db, booking_id=booking_id)

    updated_data = updated_booking.model_dump(exclude_unset=True)
    if updated_data.get("arrival_date") and updated_data.get("departure_date"):
        check = await db.execute(select(Booking).where(Booking.id != booking_id).where(
            not_(or_(
                Booking.departure_date <= updated_data.get("arrival_date"),
                Booking.arrival_date >= updated_data.get("departure_date"),
            ))
        ))
        if check.scalar_one_or_none():
            raise AlreadyExistsException("Booking already exists for this period")

    
    for key, value in updated_data.items():
        setattr(existing, key, value)
    
    await db.commit()
    await db.refresh(existing)

    return existing


async def delete_booking(db: AsyncSession, booking_id: int) -> Booking:
    """Delete and return a booking"""
    existing = await get_booking_by_id(db=db, booking_id=booking_id)
    room = await get_room_by_id(db=db, room_id=existing.room_id)

    response_data = BookingResponse.model_validate(existing)

    await db.delete(existing)
    await update_rooms_quantity(db=db, room_id=room.id, delta=+1)
    await db.commit()

    return response_data
