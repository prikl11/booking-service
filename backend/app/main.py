from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.api.router import router
from app.utils.exceptions import (
    NotAvailableException,
    NotFoundException,
    AlreadyExistsException,
    ForbiddenException,
)


app = FastAPI(title="Booking Service API")

app.include_router(router=router)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.exception_handler(NotAvailableException)
async def not_available_exception_handler(request: Request, exc: NotAvailableException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message},
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message},
    )


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": exc.message},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}