import os
import logging

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
if log_level not in LOG_LEVELS:
    print(f"Invalid log level: {log_level}. Defaulting to INFO.")
    log_level = "INFO"

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVELS[log_level])
