import logging

from PColorLogging.Drawer import get_color, ColorMode


class ExtraAdapterLogger(logging.LoggerAdapter):
    def __init__(self, logger_name: str, extra={}):
        self._logger = logging.getLogger(logger_name)
        self._makeup = None
        super(ExtraAdapterLogger, self).__init__(self._logger, extra)

    def set_maker(self, makeup_function):
        self._makeup = makeup_function

    def add_handler(self, handler: logging.Handler):
        self._logger.addHandler(handler)

    def _makeup_extra_message(self, base_extra):
        new_extra = base_extra
        if self._makeup is not None:
            _config = self._makeup(base_extra)
            if _config is not None:
                for key in _config:
                    if key in base_extra:
                        for _item_config in _config[key]:
                            new_extra[key] = get_color(_item_config) + str(new_extra[key]) + get_color(ColorMode.RESET)
        return new_extra

    def process(self, msg, kwargs):
        if "extra" in kwargs:
            copy = dict(self.extra).copy()
            copy.update(kwargs["extra"])
            kwargs["extra"] = copy
        else:
            kwargs["extra"] = self.extra
        kwargs['extra'] = self._makeup_extra_message(kwargs['extra'])
        return msg, kwargs
