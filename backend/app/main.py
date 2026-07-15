from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.api.router import router
from app.utils.exceptions import (
    NotAvailableException,
    NotFoundException,
    AlreadyExistsException,
)


app = FastAPI(title="Booking Service API")

app.include_router(router=router)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.exception_handler(NotAvailableException)
async def not_available_exception_handler(request: Request, exc: NotAvailableException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"message": exc.message},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}