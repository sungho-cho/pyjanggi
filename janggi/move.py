from typing import List, Tuple

from . import constants
from .grid import Grid
from .camp import Camp
from .piece import PieceType


class MoveSet:
    def __init__(self, moves: List[Tuple[int, int]]):
        self.moves = moves

    def __str__(self):
        return str(self.moves)

    def get_dest(self, board, origin: Grid, player: Camp):
        if self.is_valid(board, origin, player):
            row, col = (origin.row, origin.col)
            for dr, dc in self.moves:
                row += dr
                col += dc
            return Grid(row, col)
        else:
            return None

    def is_valid(self, board, origin: Grid, player: Camp):
        def is_out_of_bound(row: int, col: int):
            return (row < constants.MIN_ROW or row > constants.MAX_ROW or
                    col < constants.MIN_COL or col > constants.MAX_COL)
        origin_piece = board.get(origin.row, origin.col)
        num_hurdles = 1 if origin_piece.piece_type == PieceType.CANNON else 0
        row, col = (origin.row, origin.col)
        for i in range(len(self.moves)):
            (dr, dc) = self.moves[i]
            row += dr
            col += dc
            if is_out_of_bound(row, col):
                return False

            piece = board.get(row, col)
            # cannon cannot ever pass cannon
            if (piece and piece.piece_type == PieceType.CANNON and
                    origin_piece.piece_type == PieceType.CANNON):
                return False

            if i == len(self.moves)-1:
                # invalidate if some hurdles are left
                if num_hurdles > 0:
                    return False
                # invalidate if landing on an ally piece
                return not piece or piece.camp != player

            if piece:
                # decrement number of hurdles left when passing a piece
                num_hurdles -= 1
                if num_hurdles < 0:
                    return False
        return True
