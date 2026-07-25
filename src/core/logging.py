import logging
import sys
from typing import Literal

LogLevelStr = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LOG_FORMATS: dict[LogLevelStr, str] = {
    "DEBUG": "[%(asctime)s] %(levelname)-8s %(name)s:%(filename)s:%(lineno)d - %(message)s",
    "INFO": "[%(asctime)s] %(levelname)-8s %(name)s - %(message)s",
    "WARNING": "[%(asctime)s] %(levelname)-8s %(name)s - %(message)s",
    "ERROR": "[%(asctime)s] %(levelname)-8s %(name)s:%(filename)s:%(lineno)d - %(message)s",
    "CRITICAL": "[%(asctime)s] %(levelname)-8s %(name)s:%(filename)s:%(lineno)d - %(message)s",
}


def configure_logging(level_name: LogLevelStr = "INFO") -> None:
    """Configure the root application logger."""

    logging.basicConfig(
        level=getattr(logging, level_name, logging.INFO),
        format=LOG_FORMATS[level_name],
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
