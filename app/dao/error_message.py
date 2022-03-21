from enum import Enum, auto


class ErrorMessage(Enum):
    DUPLICATED_ID = auto()
    DUPLICATED_EMAIL = auto()
    UNKNOWN_ERROR = auto()
