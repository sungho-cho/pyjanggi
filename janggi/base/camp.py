from __future__ import annotations
from enum import IntEnum
from ..proto import log_pb2

class Camp(IntEnum):
    """
    Enum that represents two sides of the game of Janggi.
    It's just like black and white in chess except it's called cho and han.
    """
    CHO = 1
    HAN = -1
    UNDECIDED = 0

    @property
    def opponent(self) -> Camp:
        """
        Return opponent's enum. (Camp.CHO for Camp.HAN / Camp.HAN for Camp.CHO).

        Returns:
            Camp: Opponent's enum instance.
        """
        return Camp(self * -1)

    @classmethod
    def from_proto(cls, camp_proto: log_pb2.Camp) -> Camp:
        """Convert from proto Camp enum."""
        if camp_proto == log_pb2.Camp.CHO:
            return cls.CHO
        elif camp_proto == log_pb2.Camp.HAN:
            return cls.HAN
        else:
            return cls.UNDECIDED

    def to_proto(self) -> log_pb2.Camp:
        """Convert to proto Camp enum."""
        if self == Camp.CHO:
            return log_pb2.Camp.CHO
        elif self == Camp.HAN:
            return log_pb2.Camp.HAN
        else:
            raise Exception(f"Cannot convert Camp enum {self} to proto.")
        