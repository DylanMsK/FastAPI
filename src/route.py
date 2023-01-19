import logging

from fastapi import Request, Response
from fastapi.routing import APIRoute


logger = logging.getLogger("request")


class BaseAPIRoute(APIRoute):
    def get_route_handler(self):
        route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.json()
            request.state.req_body = req_body
            response: Response = await route_handler(request)
            return response

        return custom_route_handler
