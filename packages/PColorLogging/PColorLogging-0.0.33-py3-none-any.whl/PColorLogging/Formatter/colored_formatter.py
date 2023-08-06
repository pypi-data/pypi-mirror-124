import logging

from PColorLogging.Drawer import Drawer


class ColoredFormatter(logging.Formatter):
    def __init__(self, ftm, config=None, file_config=None, date_fmt='%m-%d-%Y %H:%M:%S', use_color=True):
        logging.Formatter.__init__(self, ftm, datefmt=date_fmt)
        self.drawer = Drawer(ftm, config, file_config)
        self.use_color = use_color

    def format(self, record):
        level_name = record.levelname

        if self.use_color:
            self._style._fmt = self.drawer.get_message(level_name)
        return logging.Formatter.format(self, record)
