import logging
from uvicorn.logging import ColourizedFormatter


def set_logger():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        ColourizedFormatter(
            fmt="%(asctime)s.%(msecs)03d | %(levelprefix)8s | %(module)s.%(funcName)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="%",
            use_colors=True,
        )
    )

    request_logger = logging.getLogger("request")
    request_logger.addHandler(console_handler)
