from __future__ import annotations
from enum import IntEnum

class Camp(IntEnum):
    """
    Enum that represents two sides of the game of Janggi.
    It's just like black and white in chess except it's called cho and han.
    """
    CHO = 0
    HAN = 1

    @property
    def opponent(self) -> Camp:
        """
        Return opponent's enum. (Camp.CHO for Camp.HAN / Camp.HAN for Camp.CHO).

        Returns:
            Camp: Opponent's enum instance.
        """
        return Camp(1-self)