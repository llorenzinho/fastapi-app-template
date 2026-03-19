from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from {{ values.module_name }}.core.exceptions import NotFoundException


class ErrorResponse(BaseModel):
    code: int
    error: str
    detail: str | None = None


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code=500,
            error="Internal Server Error",
        ).model_dump(),
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:  # type: ignore
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            code=404,
            detail=exc.__str__(),
            error="Not Found",
        ).model_dump(),
    )
