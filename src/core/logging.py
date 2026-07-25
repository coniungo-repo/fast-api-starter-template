import logging
from enum import IntEnum


class LogLevel(IntEnum):
    """Mapping of standard log levels to Python logging constants."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


DEBUG_FORMAT = "%(levelname)s:%(name)s:%(message)s:%(pathname)s:%(lineno)d"
DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def configure_logging(level: LogLevel = LogLevel.INFO) -> None:
    """Initializes global logging config, selecting format based on severity level."""
    logging.basicConfig(
        level=level,
        format=DEBUG_FORMAT if level == LogLevel.DEBUG else DEFAULT_FORMAT,
        force=True,
    )
