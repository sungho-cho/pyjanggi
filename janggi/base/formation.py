from enum import IntEnum


class Formation(IntEnum):
    """
    Enum class that represents 4 different formations of the game of Janggi.
    See https://en.wikipedia.org/wiki/Janggi#Setting_up for details on formations.
    In Korean terminology,
    the inner elephant setup is called Won-Ang-Ma,
    the outer elephant setup is called Yang-Gwi-Ma,
    the left elephant and right elephant setup are called Gwi-Ma.
    """
    INNER_ELEPHANT = 1
    OUTER_ELEPHANT = 2
    LEFT_ELEPHANT = 3
    RIGHT_ELEPHANT = 4
    UNDECIDED = 5