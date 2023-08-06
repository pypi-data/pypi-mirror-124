import logging

from converterpy.exception import LoggerNotFoundException

LEVEL_OUT = 100
logging.addLevelName(LEVEL_OUT, "OUT")


class Logger(logging.Logger):

    def out(self, msg, *args, **kwargs):
        if self.isEnabledFor(LEVEL_OUT):
            self._log(LEVEL_OUT, msg, args, **kwargs)


class _LogManager(object):

    DEFAULT_LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    DEFAULT_LOGGER_NAME = 'converter'

    def __init__(self):
        self.loggers = dict()

    def get_logger(self, name=DEFAULT_LOGGER_NAME):
        assert isinstance(name, str)

        if name in self.loggers:
            return self.loggers[name]

        return self.create_logger(name)

    def create_logger(self, name=DEFAULT_LOGGER_NAME, level=logging.DEBUG, log_format=DEFAULT_LOG_FORMAT):
        assert isinstance(name, str)

        logger = logging.getLogger(name)

        # ----

        handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(level)

        # ---

        self.loggers[name] = logger

        # ----

        return logger

    def override_format(self, name, log_format):
        """ override each handlers format """
        assert isinstance(name, str)
        assert isinstance(log_format, str)

        if name not in self.loggers:
            raise LoggerNotFoundException(name)

        logger = self.loggers[name]
        for handler in logger.handlers:
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)

    def override_log_level(self, name, level):
        """ override log level """
        assert isinstance(name, str)

        if name not in self.loggers:
            raise LoggerNotFoundException(name)

        self.loggers[name].setLevel(level)

# -----


logging.setLoggerClass(Logger)

LogManager = _LogManager()

