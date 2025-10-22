"""
Logging configuration for BCOS.

Provides structured logging with different levels for development and production.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, debug: bool = False, log_file: str = None) -> logging.Logger:
    """
    Set up a logger with consistent formatting.

    Args:
        name: Logger name (typically __name__)
        debug: Enable debug-level logging
        log_file: Optional file path for logging output

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set level
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console handler with color-coded formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Format: [2024-01-15 10:30:45] INFO - module_name - Message
    console_format = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)-8s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)  # Always debug in files

        file_format = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s - %(name)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def get_default_log_file() -> str:
    """Generate default log file path with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir = Path('outputs/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    return str(log_dir / f'bcos_{timestamp}.log')
