import logging
import traceback

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException

from src.exceptions import DetailedHTTPException


logger = logging.getLogger(__name__)


class BaseAPIRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_api_route_data = {"path": request.url.path, "body": None}
            if request.query_params:
                req_api_route_data["path"] += f"?{str(request.query_params)}"

            try:
                body = await request.json()
                request.state.body = body
                req_api_route_data["body"] = body
            except Exception:
                pass
            finally:
                logger.info(req_api_route_data)

            try:
                response: Response = await original_route_handler(request)
                logger.info("")
                return response
            except HTTPException as exc:
                raise exc
            except Exception as exc:
                msg = {
                    "error": str(exc),
                    "detail": traceback.format_exc(),
                }
                logger.error(msg)
                raise DetailedHTTPException(detail=str(exc))

        return custom_route_handler
