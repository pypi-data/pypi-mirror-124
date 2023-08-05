from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Direction(AutoName):
    LONG = auto()
    SHORT = auto()


class Offset(AutoName):
    OPEN = auto()
    CLOSE = auto()
    CLOSETODAY = auto()
    CLOSEYESTERDAY = auto()


class OrderStatus(AutoName):
    SUBMITTING = auto()
    NOTTRADED = auto()
    PARTTRADED = auto()
    ALLTRADED = auto()
    CANCELLED = auto()
    REJECTED = auto()


class OrderType(AutoName):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()
    FAK = auto()
    FOK = auto()


class ProductClass(AutoName):
    FUTURES = auto()
    OPTIONS = auto()
    COMBINATION = auto()


class OptionType(AutoName):
    CALL = auto()
    PUT = auto()


class Exchange(AutoName):
    CFFEX = auto()
    SHFE = auto()
    CZCE = auto()
    DCE = auto()
    INE = auto()