from fastapi import APIRouter

from app.api.routers import (
    service_router,
    hotel_router,
    hotel_images_router,
    hotel_services_router,
    hotel_staff_router,
    auth_router,
    user_router,
    room_router,
    room_services_router,
    room_images_router,
    room_beds_router,
)


router = APIRouter()

router.include_router(router=auth_router)
router.include_router(router=user_router)
router.include_router(router=service_router)
router.include_router(router=hotel_router)
router.include_router(router=hotel_images_router)
router.include_router(router=hotel_services_router)
router.include_router(router=hotel_staff_router)
router.include_router(router=room_router)
router.include_router(router=room_services_router)
router.include_router(router=room_images_router)
router.include_router(router=room_beds_router)