from enum import Enum
from typing import Any
from io import TextIOWrapper


class Level(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    file: None | TextIOWrapper | Any

    def __init__(self, file=None):
        self.file = file
        pass

    def log(
        self, *args: Any, level: Level = Level.INFO, sep: str = " ", end: str = "\n"
    ) -> None:
        print(f"[{level.value}]", *args, sep=sep, end=end, file=self.file)

    def debug(self, *args: Any, sep: str = " ", end: str = "\n") -> None:
        self.log(*args, level=Level.DEBUG, sep=sep, end=end)

    def info(self, *args: Any, sep: str = " ", end: str = "\n") -> None:
        self.log(*args, level=Level.INFO, sep=sep, end=end)

    def warning(self, *args: Any, sep: str = " ", end: str = "\n") -> None:
        self.log(*args, level=Level.WARNING, sep=sep, end=end)

    def error(self, *args: Any, sep: str = " ", end: str = "\n") -> None:
        self.log(*args, level=Level.ERROR, sep=sep, end=end)

    def critical(self, *args: Any, sep: str = " ", end: str = "\n") -> None:
        self.log(*args, level=Level.CRITICAL, sep=sep, end=end)
