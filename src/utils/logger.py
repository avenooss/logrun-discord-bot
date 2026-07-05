"""Logger setup utility."""

import logging.config
from typing import Optional

from src.config.logging_config import LOGGING_CONFIG


def setup_logging(level: Optional[str] = None) -> None:
    """Setup logging configuration.
    
    Args:
        level: Optional log level override (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    
    if level:
        logger = logging.getLogger("src")
        logger.setLevel(level.upper())
        
        for handler in logger.handlers:
            handler.setLevel(level.upper())


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
