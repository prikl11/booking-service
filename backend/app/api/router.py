from fastapi import APIRouter

from app.api.routers.services import router as service_router
from app.api.routers.hotels import router as hotel_router


router = APIRouter()

router.include_router(router=service_router)
router.include_router(router=hotel_router)