import logging
import sys

from .config.config import LOG_LEVEL, LOG_PATH


def get_logger(name: str) -> logging.Logger:
    name = name.replace("discord_bot.", "")
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if LOG_PATH != "" and LOG_PATH is not None:
        file_handler = logging.FileHandler(f"{LOG_PATH}/{name}.log", mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
