import logging
import os


def load_logger() -> logging.Logger:
    logger = logging.getLogger(__package__)
    logger.setLevel(os.getenv("LOG_LEVEL", logging.DEBUG))

    # Add a stream handler so that we see logs in the console when running tests
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    return logger
