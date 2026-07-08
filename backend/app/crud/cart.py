from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.orm import selectinload

from app.database.models import Cart
from app.database.schemas import CartCreate, CartResponse
from app.utils.exceptions import NotFoundException


async def get_all_carts(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Cart]:
    """Return a paginated list of carts"""
    result = await db.execute(select(Cart).offset(skip).limit(limit))
    return result.scalars().all()


async def get_all_carts_by_user(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Cart]:
    """Return a paginated list of carts by user's ID"""
    result = await db.execute(select(Cart).where(Cart.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()


async def get_cart_by_id(db: AsyncSession, cart_id: int) -> Cart:
    """Return cart by ID or None if not found"""
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.user))
        .where(Cart.id == cart_id)
    )
    cart = result.scalar_one_or_none()
    if not cart:
        raise NotFoundException("Cart not found")
    return cart


async def create_cart(db: AsyncSession, cart: CartCreate) -> Cart:
    """Create and return a new cart"""
    new_cart = Cart(**cart.model_dump())

    db.add(new_cart)
    await db.commit()
    await db.refresh(new_cart)

    return new_cart


async def delete_cart(db: AsyncSession, cart_id: int) -> Cart:
    """Delete and return a cart"""
    cart = await get_cart_by_id(db=db, cart_id=cart_id)

    response_data = CartResponse.model_validate(cart)

    await db.delete(cart)
    await db.commit()

    return response_data
