from fastapi import APIRouter

from app.api.routers.services import router as service_router


router = APIRouter()

router.include_router(router=service_router)