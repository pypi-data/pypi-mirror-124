import logging

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

level_to_names = logging._levelToName


def get_level_names():
    _result = []
    for key in level_to_names:
        _result.append(level_to_names[key])
    return _result


def get_level_number():
    _result = []
    for key in level_to_names:
        _result.append(key)
    return _result


def is_level(level: str or int):
    for key in level_to_names:
        if type(level) is str:
            if level_to_names[key] == level:
                return True
        if type(level) is int:
            if key == level:
                return True
    return False


def add_level_name(level: int, level_name: str):
    logging.addLevelName(level, level_name)
