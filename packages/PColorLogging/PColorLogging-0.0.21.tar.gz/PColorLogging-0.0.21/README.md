<h1 align="center">PColorLogging</h1>
<p align="center">
  The powerful python logging, you can create colorful logging and easy to add logging level or record attribute
</p>

### Getting Start
To create the logger
```pycon
import logging

from PColorLogging import DEBUG, INFO, ERROR, WARNING, CRITICAL
from PColorLogging.Drawer.color import PColor, TextMode
from PColorLogging.Formatter.colored_formatter import ColoredFormatter
from PColorLogging.Logger.Adapter.extra_adapter_logger import ExtraAdapterLogger

colored_formatter = ColoredFormatter(f"[%(asctime)s] %(levelname)s:%(phuc)s %(message)s", [
    {"config": {"message": [PColor.BLUE]}, "level": [DEBUG]},
    {"config": {"message": [PColor.BLUE, TextMode.CROSS], "phuc": [PColor.B_WHITE]}, "level": [INFO]},
    {"config": {"message": [PColor.CYAN, TextMode.UNDERLINE]}, "level": [ERROR]},
    {"config": {"message": [PColor.GREEN, TextMode.SLOW_BLINK]}, "level": [WARNING]},
    {"config": {"message": [PColor.WHITE, TextMode.FAST_BLINK]}, "level": [CRITICAL]},
    {"config": {"message": [PColor.BLUE], "levelname": [PColor.B_CYAN, PColor.WHITE]}, "level": [25]}
])

extra_logger = ExtraAdapterLogger("logger", {"phuc": ""})

console_handler = logging.StreamHandler()
console_handler.setFormatter(colored_formatter)
extra_logger.add_handler(console_handler)
extra_logger.setLevel(logging.INFO)

extra_logger.debug("this is debug", extra={"phuc": 4321})
extra_logger.info("this is info")
extra_logger.warning("this is warning")
extra_logger.error("this is error")
extra_logger.critical("this is critical")
extra_logger.log(25, "this is custom logging level")
```
