import logging
import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src import request as ctx_request


logger = logging.getLogger(__name__)


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        ctx_request.set(request)

        start = time.time()
        req_log_data = {
            "headers": dict(zip(request.headers.keys(), request.headers.values())),
            "method": request.method,
            "path": request.url.path,
        }

        if request.query_params:
            req_log_data["path"] += f"?{str(request.query_params)}"

        logger.info(req_log_data)

        response: Response = await call_next(request)

        end = time.time()
        latency = round((end - start) * 100, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Latency"] = str(latency)

        status_code = response.status_code
        res_log_data = {
            "status_code": status_code,
            "latency": latency,
        }
        logger.info(res_log_data)
        return response


class ResponseWarppingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        return await super().dispatch(request, call_next)
