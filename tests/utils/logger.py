import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from tests.utils.logger_config import LoggerConfig


class Logger:
    if not os.path.isdir(LoggerConfig.LOGS_DIR_NAME):
        os.makedirs(LoggerConfig.LOGS_DIR_NAME)

    __logger = logging.getLogger(LoggerConfig.LOGGER_NAME)
    __logger.setLevel(LoggerConfig.LOGS_LEVEL)

    __file_handler = RotatingFileHandler(
        LoggerConfig.LOGS_FILE_NAME,
        maxBytes=LoggerConfig.MAX_BYTES,
        backupCount=LoggerConfig.BACKUP_COUNT
    )
    __console_handler = logging.StreamHandler(sys.stdout)

    __formatter = logging.Formatter(
        LoggerConfig.FORMAT,
        datefmt=LoggerConfig.DATETIME_FORMAT
    )
    __file_handler.setFormatter(__formatter)
    __console_handler.setFormatter(__formatter)

    __logger.addHandler(__file_handler)
    __logger.addHandler(__console_handler)

    @staticmethod
    def info(message: str):
        Logger.__logger.info(msg=message)

    @staticmethod
    def debug(message: str):
        Logger.__logger.debug(msg=message)

    @staticmethod
    def warning(message: str):
        Logger.__logger.warning(msg=message)

    @staticmethod
    def error(message: str):
        Logger.__logger.error(msg=message)