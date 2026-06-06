
"""
Sherlock Pro - Logging Utility
"""

import logging
import sys
from pathlib import Path


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("sherlock_pro")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
