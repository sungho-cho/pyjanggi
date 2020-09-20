from piece import Piece
from grid import Grid

class Move:
    def __init__(self, piece: Piece, origin: Grid, dest: Grid):
        self.piece = piece
        self.origin = origin
        self.dest = dest
