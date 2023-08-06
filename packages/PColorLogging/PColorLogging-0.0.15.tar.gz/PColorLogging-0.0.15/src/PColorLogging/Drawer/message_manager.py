from src.PColorLogging import get_level_names


class _MessageManager:
    def __init__(self, base_message):
        self._base_message = base_message
        self._level_message_list = {}

    def get_default_message(self):
        default_message_list = []
        for _level in get_level_names():
            default_message_list[_level] = self._base_message
        return default_message_list

    def get_message(self, level):
        if level in get_level_names():
            if level in self._level_message_list:
                return self._level_message_list[level]
            else:
                return self._base_message
        return None

    def set_base_message(self, base_message):
        self._base_message = base_message

    def set_message(self, level, config_message):
        self._level_message_list[level] = config_message

    def reset_message(self):
        self._level_message_list = {}
