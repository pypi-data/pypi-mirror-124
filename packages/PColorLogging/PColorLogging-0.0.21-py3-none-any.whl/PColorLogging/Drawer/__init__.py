from src.PColorLogging import level_to_names, is_level
from src.PColorLogging.Drawer.color import get_color, ColorMode
from src.PColorLogging.Drawer.message_manager import _MessageManager
from src.PColorLogging.error import NotFoundLevel

BASE_CHARS = ['-', '+', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 's', 'f', 'd']


class Drawer:
    def __init__(self, base_message: str, config=None):
        self._base_message = base_message
        self._message = _MessageManager(base_message)
        self.config = config

        self._draw_message()

    def _detect_format_attribute(self, record_attribute: str):
        record_attribute = f"%({record_attribute})"
        index = self._base_message.find(record_attribute)
        if index == -1:
            return record_attribute
        base_index = index + len(record_attribute)
        _len = len(self._base_message)
        while base_index < _len:
            if self._base_message[base_index] in BASE_CHARS:
                record_attribute += self._base_message[base_index]
                base_index += 1
            else:
                break
        return record_attribute

    def _draw_message(self):
        if self.config is not None:
            for item in self.config:
                _temp_message = self._base_message
                for key in item['config']:
                    attribute_maker = self._detect_format_attribute(key)
                    new_attribute_maker = attribute_maker
                    _config = item['config'][key]
                    for _item_config in _config:
                        new_attribute_maker = get_color(_item_config) + new_attribute_maker + get_color(ColorMode.RESET)
                    _temp_message = _temp_message.replace(attribute_maker, new_attribute_maker)
                for _level in item['level']:
                    if _level not in level_to_names:
                        raise NotFoundLevel(_level)
                    str_level = level_to_names[_level]
                    if str_level is not None:
                        self._message.set_message(str_level, _temp_message)

    def get_message(self, level=None):
        if level is None:
            return self._base_message
        elif not is_level(level):
            return self._base_message
        else:
            return self._message.get_message(level)

    def set_config(self, config):
        self.config = config
        self._draw_message()
