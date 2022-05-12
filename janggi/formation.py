from enum import IntEnum

from .board import Board
from .piece import PieceType, Piece


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

    def make_board(self) -> Board:
        """
        Generate a half-board filled with pieces on the bottom side, based on the formation.

        Returns:
            Board: Board that contains pieces on the bottom side. 
                   Can be rotated and merged with another half-board.
        """
        board = self._initial_board()
        if self == self.OUTER_ELEPHANT:
            board.put(9, 1, Piece(PieceType.ELEPHANT))
            board.put(9, 2, Piece(PieceType.HORSE))
            board.put(9, 6, Piece(PieceType.HORSE))
            board.put(9, 7, Piece(PieceType.ELEPHANT))

        elif self == self.LEFT_ELEPHANT:
            board.put(9, 1, Piece(PieceType.ELEPHANT))
            board.put(9, 2, Piece(PieceType.HORSE))
            board.put(9, 6, Piece(PieceType.ELEPHANT))
            board.put(9, 7, Piece(PieceType.HORSE))

        elif self == self.RIGHT_ELEPHANT:
            board.put(9, 1, Piece(PieceType.HORSE))
            board.put(9, 2, Piece(PieceType.ELEPHANT))
            board.put(9, 6, Piece(PieceType.HORSE))
            board.put(9, 7, Piece(PieceType.ELEPHANT))

        elif self == self.INNER_ELEPHANT:
            board.put(9, 1, Piece(PieceType.HORSE))
            board.put(9, 2, Piece(PieceType.ELEPHANT))
            board.put(9, 6, Piece(PieceType.ELEPHANT))
            board.put(9, 7, Piece(PieceType.HORSE))
        return board

    def _initial_board(self) -> Board:
        """
        Generate initial half-board that only contains pieces whose locations are not affected by formations.

        Returns:
            Board: Half-board that contains a few initial pieces.
        """
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
