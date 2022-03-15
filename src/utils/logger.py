import logging


def configure_logger(level:int=logging.INFO) -> None:
    logging.basicConfig(level=level)

