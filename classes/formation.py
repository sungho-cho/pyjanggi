from enum import IntEnum

from .board import Board
from .piece import PieceType, Piece


class Formation(IntEnum):
    YANGGWIMA = 1
    GWIMASANG = 2
    GWIMAMA = 3
    WONWANGMA = 4

    def initialBoard(self):
        board = Board()
        board.put(7, 1, Piece(PieceType.SOLDIER))
        board.put(7, 3, Piece(PieceType.SOLDIER))
        board.put(7, 5, Piece(PieceType.SOLDIER))
        board.put(7, 7, Piece(PieceType.SOLDIER))
        board.put(7, 9, Piece(PieceType.SOLDIER))

        board.put(8, 2, Piece(PieceType.CANNON))
        board.put(8, 8, Piece(PieceType.CANNON))

        board.put(9, 5, Piece(PieceType.GENERAL))

        board.put(10, 4, Piece(PieceType.GUARD))
        board.put(10, 6, Piece(PieceType.GUARD))

        board.put(10, 1, Piece(PieceType.CHARIOT))
        board.put(10, 9, Piece(PieceType.CHARIOT))
        return board

    def makeBoard(self):
        board = self.initialBoard()
        if self == self.YANGGWIMA:
            board.put(10, 2, Piece(PieceType.ELEPHANT))
            board.put(10, 3, Piece(PieceType.HORSE))
            board.put(10, 7, Piece(PieceType.HORSE))
            board.put(10, 8, Piece(PieceType.ELEPHANT))

        elif self == self.GWIMASANG:
            board.put(10, 2, Piece(PieceType.ELEPHANT))
            board.put(10, 3, Piece(PieceType.HORSE))
            board.put(10, 7, Piece(PieceType.ELEPHANT))
            board.put(10, 8, Piece(PieceType.HORSE))

        elif self == self.GWIMAMA:
            board.put(10, 2, Piece(PieceType.HORSE))
            board.put(10, 3, Piece(PieceType.ELEPHANT))
            board.put(10, 7, Piece(PieceType.HORSE))
            board.put(10, 8, Piece(PieceType.ELEPHANT))

        elif self == self.WONWANGMA:
            board.put(10, 2, Piece(PieceType.HORSE))
            board.put(10, 3, Piece(PieceType.ELEPHANT))
            board.put(10, 7, Piece(PieceType.ELEPHANT))
            board.put(10, 8, Piece(PieceType.HORSE))
        return board
