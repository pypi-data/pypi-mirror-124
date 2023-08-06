class NotFoundLevel(Exception):
    def __init__(self, _level):
        self.level = _level

    def __str__(self):
        if self.level is None:
            return "Not found level"
        else:
            return f"Not found level: {self.level}"
