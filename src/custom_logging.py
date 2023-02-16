import logging
import sys
from pathlib import Path
from loguru import logger
import json

from pydantic import BaseModel, validator


from src import request as ctx_request


class LoggerConfig(BaseModel):
    path: str
    filename: str
    level: str
    rotation: str
    format: str

    @validator("level")
    def level_upper(cls, v):
        return v.upper()

    @property
    def filepath(self):
        return Path(self.path) / self.filename


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        request = ctx_request.value
        request_id = "system" if request is None else request.state.request_id
        log = logger.bind(request_id=request_id)
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls, config_path: Path):
        config = cls.load_logging_config(config_path)
        logger = cls.customize_logging(config=config)
        return logger

    @classmethod
    def customize_logging(cls, config: dict):

        logger.remove()

        # 기본 로깅
        default_config = LoggerConfig(**config.get("default"))
        logger.add(sys.stdout, level=default_config.level, format=default_config.format)
        logger.add(
            default_config.filepath,
            rotation=default_config.rotation,
            level=default_config.level,
            format=default_config.format,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        for _log in ["uvicorn", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        for _log in ["uvicorn.access", "uvicorn.error"]:
            _logger = logging.getLogger(_log)
            _logger.disabled = True

        return logger.bind(request_id=None)

    # @classmethod
    # def customize_logging(cls, filepath: Path, level: str, rotation: str, retention: str, format: str):

    #     logger.remove()
    #     logger.add(sys.stdout, level=level.upper(), format=format)
    #     logger.add(
    #         str(filepath),
    #         rotation=rotation,
    #         retention=retention,
    #         level=level.upper(),
    #         format=format,
    #     )
    #     logging.basicConfig(handlers=[InterceptHandler()], level=0)
    #     # logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    #     # logging.getLogger("uvicorn.error").disabled = True

    #     for _log in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
    #         _logger = logging.getLogger(_log)
    #         _logger.handlers = [InterceptHandler()]

    #     return logger.bind(request_id=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
