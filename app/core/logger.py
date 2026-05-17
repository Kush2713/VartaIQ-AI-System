import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Format used by both handlers
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # =====================================
    # HANDLER 1 — Terminal (what you see now)
    # =====================================

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # =====================================
    # HANDLER 2 — Log File
    # Saves to logs/app.log
    # Max size: 5MB, keeps last 3 files
    # =====================================

    os.makedirs("logs", exist_ok=True)

    file_handler = RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3,               # keeps app.log, app.log.1, app.log.2
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger