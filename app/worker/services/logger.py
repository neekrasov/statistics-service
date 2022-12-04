import logging


def init_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(
        "[WORKER] - %(asctime)s - %(name)s - %(levelname)s - [%(message)s]"
    ))
    logger.addHandler(stream_handler)
    return logger
