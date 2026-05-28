import os


class LoggerConfig:
    LOGS_DIR_NAME = "logs"
    LOGGER_NAME = "TestLogger"
    LOGS_FILE_NAME = LOGS_DIR_NAME + os.sep + "test.log"
    LOGS_LEVEL = 10
    MAX_BYTES = 1_000_000
    BACKUP_COUNT = 10
    FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"