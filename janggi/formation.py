from enum import IntEnum

from .board import Board
from .piece import PieceType, Piece


class Formation(IntEnum):
    YANGGWIMA = 1
    GWIMASANG = 2
    GWIMAMA = 3
    WONWANGMA = 4

    def initial_board(self):
        board = Board()
        board.put(6, 0, Piece(PieceType.SOLDIER))
        board.put(6, 2, Piece(PieceType.SOLDIER))
        board.put(6, 4, Piece(PieceType.SOLDIER))
        board.put(6, 6, Piece(PieceType.SOLDIER))
        board.put(6, 8, Piece(PieceType.SOLDIER))

        board.put(7, 1, Piece(PieceType.CANNON))
        board.put(7, 7, Piece(PieceType.CANNON))

        board.put(8, 4, Piece(PieceType.GENERAL))

        board.put(9, 3, Piece(PieceType.GUARD))
        board.put(9, 5, Piece(PieceType.GUARD))

        board.put(9, 0, Piece(PieceType.CHARIOT))
        board.put(9, 8, Piece(PieceType.CHARIOT))
        return board

    def make_board(self):
        board = self.initial_board()
        if self == self.YANGGWIMA:
            board.put(9, 1, Piece(PieceType.ELEPHANT))
            board.put(9, 2, Piece(PieceType.HORSE))
            board.put(9, 6, Piece(PieceType.HORSE))
            board.put(9, 7, Piece(PieceType.ELEPHANT))

        elif self == self.GWIMASANG:
            board.put(9, 1, Piece(PieceType.ELEPHANT))
            board.put(9, 2, Piece(PieceType.HORSE))
            board.put(9, 6, Piece(PieceType.ELEPHANT))
            board.put(9, 7, Piece(PieceType.HORSE))

        elif self == self.GWIMAMA:
            board.put(9, 1, Piece(PieceType.HORSE))
            board.put(9, 2, Piece(PieceType.ELEPHANT))
            board.put(9, 6, Piece(PieceType.HORSE))
            board.put(9, 7, Piece(PieceType.ELEPHANT))

        elif self == self.WONWANGMA:
            board.put(9, 1, Piece(PieceType.HORSE))
            board.put(9, 2, Piece(PieceType.ELEPHANT))
            board.put(9, 6, Piece(PieceType.ELEPHANT))
            board.put(9, 7, Piece(PieceType.HORSE))
        return board
