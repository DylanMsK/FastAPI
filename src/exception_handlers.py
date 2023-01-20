from fastapi import Request, status
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.response import ErrorResponse


async def request_validation_exception_handler(request: Request, exc: ValueError):
    content = ErrorResponse(
        error={
            "code": "COM422",
            "message": str(exc),
        }
    )
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content.dict())


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)

    content = ErrorResponse(
        error={
            "code": exc.status_code,
            "message": exc.detail or str(exc),
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        headers=headers,
        content=content.dict(),
    )
