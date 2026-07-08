from fastapi import APIRouter

from app.api.routers.services import router as service_router
from app.api.routers.hotels import router as hotel_router
from app.api.routers.hotel_images import router as hotel_images_router
from app.api.routers.hotel_services import router as hotel_services_router


router = APIRouter()

router.include_router(router=service_router)
router.include_router(router=hotel_router)
router.include_router(router=hotel_images_router)
router.include_router(router=hotel_services_router)