import logging
from loguru import logger
from uvicorn.logging import ColourizedFormatter

from src import request as ctx_request


class InjectingFilter(logging.Filter):
    """
    Injecting Request ID
    """

    def filter(self, record):
        request = ctx_request.value
        record.request_id = request.state.request_id
        return True


class CustomFormatter(ColourizedFormatter):
    def __init__(self, fmt, datefmt="%Y-%m-%d %H:%M:%S", style="%", use_colors=True):
        super().__init__(fmt, datefmt, style, use_colors)


injecting_filter = InjectingFilter()

console_formatter = CustomFormatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelprefix)8s | %(module)s.%(funcName)s | %(request_id)s | %(message)s",
)
request_formatter = CustomFormatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelprefix)8s | %(name)s | %(request_id)s | %(message)s",
)
service_formatter = CustomFormatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelprefix)8s | %(module)s.%(funcName)s(%(lineno)s) | %(request_id)s | %(message)s",
)


def set_logger():
    request_handler = logging.StreamHandler()
    request_handler.setFormatter(request_formatter)

    # middlerware logger
    middleware_logger = logging.getLogger("middleware")
    middleware_logger.addFilter(injecting_filter)
    middleware_logger.addHandler(request_handler)

    # router logger
    router_logger = logging.getLogger("router")
    router_logger.addFilter(injecting_filter)
    router_logger.addHandler(request_handler)

    # service logger
    service_handler = logging.StreamHandler()
    service_handler.setFormatter(service_formatter)
    service_logger = logging.getLogger("service")
    service_logger.addFilter(injecting_filter)
    service_logger.addHandler(service_handler)
