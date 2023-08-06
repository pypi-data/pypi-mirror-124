from src.PColorLogging.Drawer.color.color_code import _ColorModeCode, _TextModeCode, _ForegroundCode, _BackgroundCode


class ColorMode:
    RESET = "reset"
    BOLD = "bold"
    DARK = "dark"


class TextMode:
    ITALIC = "italic"
    UNDERLINE = "underline"
    SLOW_BLINK = "slow_blink"
    FAST_BLINK = "fast_blink"
    REVERSE = "reverse"
    HIDE = "hide"
    CROSS = "cross"


class PColor:
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    PURPLE = "purple"
    CYAN = "cyan"
    WHITE = "white"
    B_BLACK = "b_black"
    B_RED = "b_red"
    B_GREEN = "b_green"
    B_YELLOW = "b_yellow"
    B_BLUE = "b_blue"
    B_PURPLE = "b_purple"
    B_CYAN = "b_cyan"
    B_WHITE = "b_white"


def get_color(key):
    if key == ColorMode.RESET:
        return _ColorModeCode.RESET
    elif key == ColorMode.BOLD:
        return _ColorModeCode.BOLD
    elif key == ColorMode.DARK:
        return _ColorModeCode.DARK
    elif key == TextMode.ITALIC:
        return _TextModeCode.ITALIC
    elif key == TextMode.UNDERLINE:
        return _TextModeCode.UNDERLINE
    elif key == TextMode.SLOW_BLINK:
        return _TextModeCode.SLOW_BLINK
    elif key == TextMode.FAST_BLINK:
        return _TextModeCode.FAST_BLINK
    elif key == TextMode.REVERSE:
        return _TextModeCode.REVERSE
    elif key == TextMode.HIDE:
        return _TextModeCode.HIDE
    elif key == TextMode.CROSS:
        return _TextModeCode.CROSS
    elif key == PColor.BLACK:
        return _ForegroundCode.BLACK
    elif key == PColor.RED:
        return _ForegroundCode.RED
    elif key == PColor.GREEN:
        return _ForegroundCode.GREEN
    elif key == PColor.YELLOW:
        return _ForegroundCode.YELLOW
    elif key == PColor.BLUE:
        return _ForegroundCode.BLUE
    elif key == PColor.PURPLE:
        return _ForegroundCode.PURPLE
    elif key == PColor.CYAN:
        return _ForegroundCode.CYAN
    elif key == PColor.WHITE:
        return _ForegroundCode.WHITE
    elif key == PColor.B_BLACK:
        return _BackgroundCode.BLACK
    elif key == PColor.B_RED:
        return _BackgroundCode.RED
    elif key == PColor.B_GREEN:
        return _BackgroundCode.GREEN
    elif key == PColor.B_YELLOW:
        return _BackgroundCode.YELLOW
    elif key == PColor.B_BLUE:
        return _BackgroundCode.BLUE
    elif key == PColor.B_PURPLE:
        return _BackgroundCode.PURPLE
    elif key == PColor.B_CYAN:
        return _BackgroundCode.CYAN
    elif key == PColor.B_WHITE:
        return _BackgroundCode.WHITE
    else:
        raise Exception
