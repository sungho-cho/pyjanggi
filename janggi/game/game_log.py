from typing import List, Tuple

from ..base.board import Board
from ..base.camp import Camp
from ..base.formation import Formation
from ..base.location import Location

class GameLog:
    """Simple class that represents list of moves made in a janggi game."""
    def __init__(self, cho_formation: Formation, han_formation: Formation, 
        bottom_camp: Camp, moves: List[Tuple[Location, Location]]):
        self.board = Board.full_board_from_formations(
            cho_formation, han_formation, bottom_camp)
        self.moves = moves
        self.board_logs = [self.board.copy()]
        self._set_board_logs()
        self.index = 0

    def _set_board_logs(self):
        for origin, dest in self.moves:
            self.board.move(origin, dest)
            self.board_logs.append(self.board.copy())

    def next(self) -> Board:
        if self.index >= len(self.board_logs) - 1:
            raise StopIteration
        self.index += 1
        board = self.board_logs[self.index]
        return board

    def prev(self) -> Board:
        if self.index <= 0:
            raise StopIteration
        self.index -= 1
        board = self.board_logs[self.index]
        return board
