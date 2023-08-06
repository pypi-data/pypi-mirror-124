import datetime

import logging
from pathlib import Path

from typing import Any

# TODO find a better way to make it suitable for python 3.7 as well
try:
    from typing import Literal
except ImportError:
    pass


class RLogger:

    def __init__(self, directory_path=None):
        # type: (Path | str) -> None
        """

        :param directory_path: path of the directory that we want to save our logs
        """

        # loggers
        logger = logging.getLogger('r_logger')
        logger.setLevel(logging.DEBUG)

        self._formatters = []
        self._stdout_handlers = []
        self._file_handlers = []
        self._logger = logger

        self.add_formatter("{asctime} - {levelname} - {message}", style='{')
        self.add_stream_handler()

        if directory_path:
            self.add_file_handler(directory_path)

    def add_formatter(self, fmt=None, datefmt=None, style='%', formatter=None, **kwargs):
        # type: (str, str, Literal['%', '$', '{'], logging.Formatter, dict['str', Any]) -> logging.Formatter
        """
        gets or creates a formatter an add it to formatters

        :param fmt: message format string
        :param datefmt: date format string
        :param style: formatting style: '%', '$', '{'
        :param formatter: adds a created formatter
        :keyword validate: if it's true, incorrect or mismatched style and fmt will raise a ValueError
        :return: created Formatter
        """
        # TODO find a better way to make it suitable for python 3.7 as well (valid is in kwargs)
        if formatter is None:
            formatter = logging.Formatter(fmt, datefmt, style, **kwargs)
        self._formatters.append(formatter)
        return formatter

    def add_stream_handler(self, formatter=None):
        # type: (logging.Formatter | int | None) -> logging.StreamHandler
        """
        creates a new stream handler and add it to the main logger

        :param formatter: to use costume formatter or previous formatters
        :return: created StreamHandler
        """
        # todo writing test
        if formatter is None:
            formatter = self._formatters[0]

        # todo writing test
        if isinstance(formatter, int):
            formatter = self._formatters[formatter]

        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.DEBUG)

        stdout_handler.setFormatter(formatter)

        self._stdout_handlers.append(stdout_handler)
        self._logger.addHandler(stdout_handler)

        return stdout_handler

    def add_file_handler(self, directory_path, formatter=None):
        # type: (str | Path, logging.Formatter | int | None) -> logging.FileHandler
        """
        creates a new file handler and add it to the main logger

        :param directory_path: path of the directory that using for saving log files
        :param formatter: to use costume formatter or previous formatters
        :return: created FileHandler
        """
        # todo writing test
        if formatter is None:
            formatter = self._formatters[0]

        # todo writing test
        if isinstance(formatter, int):
            formatter = self._formatters[formatter]

        directory_path = Path(directory_path)
        directory_path.mkdir(parents=True, exist_ok=True)

        now_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        path_log = directory_path.joinpath(f'log_{now_str}.log')
        file_handler = logging.FileHandler(path_log)

        file_handler.setFormatter(formatter)

        self._file_handlers.append(file_handler)
        self._logger.addHandler(file_handler)

        return file_handler

    def remove_file_handlers(self):
        """
        removes all file handlers

        :return:
        """
        for file_handler in self._file_handlers:
            self._logger.removeHandler(file_handler)

        self._file_handlers = []

    def info(self, message, *args, **kwargs):
        # type: (str, tuple[Any], dict['str', Any]) -> None
        """
        log a message with info level

        :param message: message to log
        :param args: log args
        :param kwargs: log kwargs
        :return:
        """
        self._logger.info(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        # type: (str, tuple[Any], dict['str', Any]) -> None
        """
        log a message with debug level

        :param message: message to log
        :param args: log args
        :param kwargs: log kwargs
        :return:
        """
        self._logger.debug(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        # type: (str, tuple[Any], dict['str', Any]) -> None
        """
        log a message with warning level

        :param message: message to log
        :param args: log args
        :param kwargs: log kwargs
        :return:
        """
        self._logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        # type: (str, tuple[Any], dict['str', Any]) -> None
        """
        log a message with error level

        :param message: message to log
        :param args: log args
        :param kwargs: log kwargs
        :return:
        """
        self._logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        # type: (str, tuple[Any], dict['str', Any]) -> None
        """
        log a message with critical level

        :param message: message to log
        :param args: log args
        :param kwargs: log kwargs
        :return:
        """
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        # type: (str, tuple[Any], dict['str', Any]) -> None
        """
        log a message with exception level

        :param message: message to log
        :param args: log args
        :param kwargs: log kwargs
        :return:
        """
        self._logger.exception(message, *args, **kwargs)
