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

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.disabled = True
    # for hdlr in uvicorn_access_logger.handlers[:]:  # remove all old handlers
    #     uvicorn_access_logger.removeHandler(hdlr)
    # uvicorn_access_logger.addHandler(console_handler)


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt: str, datefmt: str = None):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
