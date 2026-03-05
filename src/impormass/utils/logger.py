import logging
from ..config import APP_ENV

_fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_level = logging.DEBUG if APP_ENV == "dev" else logging.INFO

logging.basicConfig(format=_fmt, level=_level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
