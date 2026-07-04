import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import router
from app.utils.exceptions import (
    NotAvailablseException,
    NotFoundException,
    AlreadyExistsException,
)


app = FastAPI()

app.include_router(router=router)


@app.exception_handler(NotAvailablseException)
async def not_available_exception_handler(request: Request, exc: NotAvailablseException):
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