<h1 align="center">PColorLogging</h1>
The powerful python logging, you can create colorful logging and easy to add logging level or record attribute

![demo](./resources/demo.png)

## Reference
- [Installation](#installation)
- [Usage](#usage)

---
### Installation <a name="installation"></a>
PColorLogging can be installed using pip as follows:
```shell
pip install PColorLogging
```

---
### Usage <a name="usage"></a>
Here’s an example of how easy it is to get started:
```python
import logging

from PColorLogging import DEBUG, INFO, ERROR, WARNING, CRITICAL, add_level_name
from PColorLogging.Drawer.color import PColor, TextMode
from PColorLogging.Formatter.colored_formatter import ColoredFormatter

add_level_name(25, "custom")

colored_formatter = ColoredFormatter(f"[%(asctime)s] %(levelname)s: %(message)s", [
    {"config": {"message": [PColor.WHITE]}, "level": [DEBUG]},
    {"config": {"message": [PColor.GREEN], "custom": [PColor.B_WHITE]}, "level": [INFO]},
    {"config": {"message": [PColor.YELLOW]}, "level": [WARNING]},
    {"config": {"message": [PColor.RED, TextMode.UNDERLINE]}, "level": [ERROR]},
    {"config": {"message": [PColor.CYAN, TextMode.CROSS]}, "level": [CRITICAL]},
    {"config": {"message": [PColor.PURPLE]}, "level": [25]},
    {"config": {"asctime": [PColor.BLUE, PColor.B_WHITE]}, "level": 
        [DEBUG, INFO, WARNING, ERROR, CRITICAL, 25]}
])

logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setFormatter(colored_formatter)

logger.addHandler(console_handler)
logger.setLevel(DEBUG)

logger.debug("this is debug")
logger.info("this is info")
logger.warning("this is warning")
logger.error("this is error")
logger.critical("this is critical")
logger.log(25, "this is custom")
```

If you want to add custom record attribute, you should use `ExtraAdapterLogger`
```python
import logging

from PColorLogging import DEBUG, INFO, ERROR, WARNING, CRITICAL, add_level_name
from PColorLogging.Drawer.color import PColor, TextMode
from PColorLogging.Formatter.colored_formatter import ColoredFormatter
from PColorLogging.Logger.Adapter.extra_adapter_logger import ExtraAdapterLogger

add_level_name(25, "custom")

colored_formatter = ColoredFormatter(f"[%(asctime)s] %(levelname)s: %(att1)s %(att2)s %(message)s", [
    {"config": {"message": [PColor.WHITE]}, "level": [DEBUG]},
    {"config": {"message": [PColor.GREEN], "custom": [PColor.B_WHITE]}, "level": [INFO]},
    {"config": {"message": [PColor.YELLOW]}, "level": [WARNING]},
    {"config": {"message": [PColor.RED, TextMode.UNDERLINE]}, "level": [ERROR]},
    {"config": {"message": [PColor.CYAN, TextMode.CROSS]}, "level": [CRITICAL]},
    {"config": {"message": [PColor.PURPLE]}, "level": [25]},
    {"config": {"asctime": [PColor.BLUE, PColor.B_WHITE]}, "level": 
        [DEBUG, INFO, WARNING, ERROR, CRITICAL, 25]}
])

console_handler = logging.StreamHandler()
console_handler.setFormatter(colored_formatter)

extra_logger = ExtraAdapterLogger("logger", {"att1": "", "att2": ""})

extra_logger.add_handler(console_handler)
extra_logger.setLevel(DEBUG)

extra_logger.debug("this is debug", extra={"att1": "att1-debug"})
extra_logger.info("this is info", extra={"att2": "att2-info"})
extra_logger.warning("this is warning", extra={"att1": "att1", "att2": "att2"})
extra_logger.error("this is error")
extra_logger.critical("this is critical")
extra_logger.log(25, "this is custom")
```
And then, you want to add maker function to `ExtraAdapterLogger`, you can use `set_maker` function
```python
def makeup(base_extra):
    if "att1" in base_extra:
        if base_extra['att1'] == "att1-debug":
            return {"att1": [PColor.GREEN, PColor.B_YELLOW]}
    if "att2" in base_extra:
        if base_extra['att2'] == "att2-info":
            return {"att2": [PColor.B_CYAN, PColor.YELLOW]}
    return None

extra_logger.set_maker(makeup)
```
Full example in [here](/example)
