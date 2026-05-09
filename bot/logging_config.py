import logging
import os
from datetime import datetime

LOG_DIR = "logs"

def setup_logger(name: str = "trading_bot") -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    log_filename = os.path.join(LOG_DIR, f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # File handler — full detail
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_fmt)

        # Console handler — INFO and above only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_fmt = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_fmt)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
