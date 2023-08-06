import logging


class ExtraAdapterLogger(logging.LoggerAdapter):
    def __init__(self, logger, extra={}):
        super(ExtraAdapterLogger, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        if "extra" in kwargs:
            copy = dict(self.extra).copy()
            copy.update(kwargs["extra"])
            kwargs["extra"] = copy
        else:
            kwargs["extra"] = self.extra
        return msg, kwargs
