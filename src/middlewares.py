import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import StreamingResponse


logger = logging.getLogger("request")


class CustomHTTPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> StreamingResponse:
        log_data = {
            "headers": dict(zip(request.headers.keys(), request.headers.values())),
            "method": request.method,
            "path": request.url.path,
        }

        if request.method == "GET":
            if request.url.query:
                log_data["path"] += f"?{request.url.query}"
        elif request.method in ["POST", "PUT", "DELETE"]:
            pass
        response: StreamingResponse = await call_next(request)
        logger.info(msg=log_data)
        return response
