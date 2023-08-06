import logging


class ExtraAdapterLogger(logging.LoggerAdapter):
    def __init__(self, logger_name: str, extra={}):
        self._logger = logging.getLogger(logger_name)
        super(ExtraAdapterLogger, self).__init__(self._logger, extra)

    def add_handler(self, handler: logging.Handler):
        self._logger.addHandler(handler)

    def process(self, msg, kwargs):
        if "extra" in kwargs:
            copy = dict(self.extra).copy()
            copy.update(kwargs["extra"])
            kwargs["extra"] = copy
        else:
            kwargs["extra"] = self.extra
        return msg, kwargs
