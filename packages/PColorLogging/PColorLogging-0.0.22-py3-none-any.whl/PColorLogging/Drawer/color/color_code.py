class _BaseColorCode:
    pass


class _ColorModeCode(_BaseColorCode):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DARK = "\033[2m"


class _TextModeCode(_BaseColorCode):
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    SLOW_BLINK = "\033[5m"
    FAST_BLINK = "\033[6m"
    REVERSE = "\033[7m"
    HIDE = "\033[8m"
    CROSS = "\033[9m"


class _ForegroundCode(_BaseColorCode):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class _BackgroundCode(_BaseColorCode):
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    PURPLE = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
