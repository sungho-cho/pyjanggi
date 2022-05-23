from typing import List, Tuple, Optional

from ..base.board import Board
from ..base.camp import Camp
from ..base.formation import Formation
from ..base.location import Location
from ..proto import log_pb2


class GameLog:
    """Simple class that represents list of moves made in a janggi game."""

    def __init__(self, cho_formation: Formation, han_formation: Formation,
                 bottom_camp: Camp, moves: Optional[List[Tuple[Location, Location]]] = []):
        self.cho_formation = cho_formation
        self.han_formation = han_formation
        self.bottom_camp = bottom_camp
        self.move_log = moves
        self.board_log = []
        self.index = 0

    def add_move(self, move: Tuple[Location, Location]):
        """
        Add a single move to the move log

        Args:
            move (Tuple[Location ,Location]): _description_
        """
        self.move_log.append(move)

    def generate_board_log(self):
        board = Board.full_board_from_formations(
            self.cho_formation, self.han_formation, self.bottom_camp)
        self.board_log = [board.copy()]
        for origin, dest in self.move_log:
            board.move(origin, dest)
            self.board_log.append(board.copy())
        self.index = 0

    @classmethod
    def from_proto(cls, log_proto: log_pb2.Log):
        """Convert from proto Log message."""
        cho_formation = Formation.from_proto(log_proto.cho_formation)
        han_formation = Formation.from_proto(log_proto.han_formation)
        bottom_camp = Camp.from_proto(log_proto.bottom_camp)

        moves = []
        for move_proto in log_proto.moves:
            origin = Location.from_proto(move_proto.origin)
            dest = Location.from_proto(move_proto.dest)
            moves.append((origin, dest))
        return cls(cho_formation, han_formation, bottom_camp, moves)

    def to_proto(self):
        """Convert to proto Log message."""
        log_proto = log_pb2.Log()
        log_proto.cho_formation = self.cho_formation.to_proto()
        log_proto.han_formation = self.han_formation.to_proto()
        log_proto.bottom_camp = self.bottom_camp.to_proto()
        for origin, dest in self.move_log:
            move_proto = log_proto.moves.add()
            move_proto.origin.CopyFrom(origin.to_proto())
            move_proto.dest.CopyFrom(dest.to_proto())
        return log_proto

    def next(self) -> Board:
        """Used to access the next board when iterating through self.board_logs."""
        if self.index >= len(self.board_log) - 1:
            raise StopIteration
        self.index += 1
        board = self.board_log[self.index]
        return board

    def prev(self) -> Board:
        """Used to access the previous board when iterating through self.board_logs."""
        if self.index <= 0:
            raise StopIteration
        self.index -= 1
        board = self.board_log[self.index]
        return board
