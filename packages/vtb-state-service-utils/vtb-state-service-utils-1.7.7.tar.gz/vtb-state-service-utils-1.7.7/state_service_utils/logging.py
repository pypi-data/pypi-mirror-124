import logging.handlers


def create_logger(logger_name: str):
    return logging.getLogger(logger_name)
