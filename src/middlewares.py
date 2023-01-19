import logging
import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


logger = logging.getLogger("request")


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()
        log_data = {
            "id": request_id,
            "headers": dict(zip(request.headers.keys(), request.headers.values())),
            "method": request.method,
            "path": request.url.path,
        }

        if request.query_params:
            log_data["path"] += f"?{str(request.query_params)}"

        response: Response = await call_next(request)

        end = time.time()
        latency = round((end - start) * 100, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Latency"] = str(latency)

        if hasattr(request.state, "req_body"):
            req_body = request.state.req_body
        else:
            req_body = None

        log_data["status_code"] = response.status_code
        log_data["latency"] = latency
        log_data["req_body"] = req_body
        logger.info(msg=log_data)
        return response


class ResponseWarppingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        return await super().dispatch(request, call_next)
