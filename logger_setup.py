import logging
import pathlib


def setup_logger(name, log_file, level=logging.INFO, mode="a") -> logging.getLogger():
    """
    To set up a few loggers
    :param mode: file open mode
    :param name: name of the logger
    :param log_file: name of the output file
    :param level: logger level
    :return:
    """
    formatter = logging.Formatter('%(asctime)s %(message)s')
    log_dir = str(pathlib.Path(__file__).parent) + "\\logs\\"
    log_fname = log_dir + log_file
    handler = logging.FileHandler(log_fname, mode)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
