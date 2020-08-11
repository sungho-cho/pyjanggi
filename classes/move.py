from piece import Piece
from grid import Grid


class Move:
    def __init__(self, piece: Piece, start: Grid, dest: Grid):
        self.piece = piece
        self.start = start
        self.dest = dest
