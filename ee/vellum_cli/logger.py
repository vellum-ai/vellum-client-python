import logging
import os


class CLIFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    white = "\33[37m"
    reset = "\x1b[0m"
    message_format = "%(message)s"

    FORMATS = {
        logging.DEBUG: white + message_format + reset,
        logging.INFO: grey + message_format + reset,
        logging.WARNING: yellow + message_format + reset,
        logging.ERROR: red + message_format + reset,
        logging.CRITICAL: bold_red + message_format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def load_cli_logger() -> logging.Logger:
    logger = logging.getLogger(__package__)
    logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

    handler = logging.StreamHandler()
    handler.setFormatter(CLIFormatter())
    logger.addHandler(handler)

    return logger
