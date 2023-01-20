import logging
import traceback

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException

from src.exceptions import DetailedHTTPException


logger = logging.getLogger("request")


class BaseAPIRoute(APIRoute):
    def get_route_handler(self):
        route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.json()
            request.state.req_body = req_body
            try:
                response: Response = await route_handler(request)
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
