from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence

from app.database.models import Service
from app.database.schemas import ServiceCreate, ServiceUpdate
from app.utils.exceptions import NotAvailablseException, NotFoundException, AlreadyExistsException


async def get_all_services(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
) -> Sequence[Service]:
    """Return a paginated list of services"""
    result = await db.execute(select(Service).offset(skip).limit(limit))
    return result.scalars().all()


async def get_service_by_id(db: AsyncSession, service_id: int) -> Service:
    """Return a service by ID or None if not found"""
    result = await db.get(Service, service_id)
    if not result:
        raise NotFoundException("Service not found")
    return result


async def create_service(db: AsyncSession, service: ServiceCreate) -> Service:
    """Create and return a new service"""
    existing = await db.execute(select(Service).where(Service.name == service.name))
    if existing.scalar_one_or_none():
        raise AlreadyExistsException("Service already exists")
    
    created_service = Service(**service.model_dump())

    db.add(created_service)
    await db.commit()
    await db.refresh(created_service)

    return created_service


async def update_service(
        db: AsyncSession,
        service_id: int,
        updated_service: ServiceUpdate,
) -> Service:
    """Update and return a service"""
    service = await get_service_by_id(db=db, service_id=service_id)

    for key, value in updated_service.model_dump(exclude_unset=True).items():
        setattr(service, key, value)

    await db.commit()
    await db.refresh(service)

    return service


async def delete_service(db: AsyncSession, service_id: int) -> Service:
    """Delete and return a service"""
    service = await get_service_by_id(db=db, service_id=service_id)

    db.delete(service)
    await db.commit()

    return service