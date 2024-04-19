from common.domain.log.loggerService import LoggerService

import logging
from logging.handlers import TimedRotatingFileHandler


class BasicLoggerService(LoggerService):

    def __init__(self):
        # Configurar el registro para mensajes de nivel INFO
        self.__logger_info = logging.getLogger("info_logger")
        self.__logger_info.setLevel(logging.INFO)

        self.__info_handler = TimedRotatingFileHandler(
            "audit.log", when="midnight", interval=1, backupCount=7
        )
        self.__info_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.__logger_info.addHandler(self.__info_handler)

        # Configurar el registro para mensajes de nivel WARNING
        self.__logger_warning = logging.getLogger("warning_logger")
        self.__logger_warning.setLevel(logging.WARNING)

        self.__warning_handler = TimedRotatingFileHandler(
            "errors.log", when="midnight", interval=1, backupCount=7
        )
        self.__warning_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.__logger_warning.addHandler(self.__warning_handler)

    def log_warning(self, message: str):
        self.__logger_warning.warning(message)

    def log_info(self, message: str):
        self.__logger_info.info(message)
