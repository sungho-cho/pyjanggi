from __future__ import annotations
from enum import IntEnum
from ..proto import log_pb2


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

    @classmethod
    def from_proto(cls, formation_proto: log_pb2.Formation) -> Formation:
        """Convert from proto Formation enum."""
        if formation_proto == log_pb2.Formation.INNER_ELEPHANT:
            return cls.INNER_ELEPHANT
        elif formation_proto == log_pb2.Formation.OUTER_ELEPHANT:
            return cls.OUTER_ELEPHANT
        if formation_proto == log_pb2.Formation.LEFT_ELEPHANT:
            return cls.LEFT_ELEPHANT
        elif formation_proto == log_pb2.Formation.RIGHT_ELEPHANT:
            return cls.RIGHT_ELEPHANT
        else:
            return cls.UNDECIDED

    def to_proto(self) -> log_pb2.Formation:
        """Convert to proto Formation enum."""
        if self == Formation.INNER_ELEPHANT:
            return log_pb2.Formation.INNER_ELEPHANT
        elif self == Formation.OUTER_ELEPHANT:
            return log_pb2.Formation.OUTER_ELEPHANT
        elif self == Formation.LEFT_ELEPHANT:
            return log_pb2.Formation.LEFT_ELEPHANT
        elif self == Formation.RIGHT_ELEPHANT:
            return log_pb2.Formation.RIGHT_ELEPHANT
        else:
            raise Exception(f"Cannot convert Formation enum {self} to proto.")