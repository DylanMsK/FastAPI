import logging
import traceback

from fastapi import Request, Response
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from src.exceptions import DetailedHTTPException


logger = logging.getLogger("request")


class BaseAPIRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                req_body = await request.json()
                request.state.req_body = req_body
            except Exception:
                pass

            try:
                response: Response = await original_route_handler(request)
                return response
            except HTTPException as exc:
                raise exc
            except Exception as exc:
                msg = {
                    "id": request.state.request_id,
                    "detail": traceback.format_exc(),
                }
                logger.error(msg)
                raise DetailedHTTPException(detail=str(exc))

        return custom_route_handler
