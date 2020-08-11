from enum import Enum


class PieceType(Enum):
    GENERAL = 1
    GUARD = 2
    HORSE = 3
    ELEPHANT = 4
    CHARIOT = 5
    CANNON = 6
    SOLDIER = 7


class Piece:
    def __init__(self, pieceType: PieceType):
        self.pieceType = pieceType
        self.camp = None

    def setCamp(self, camp):
        self.camp = camp

    def possibleMoves(self):
        moves = []

        if self.pieceType == PieceType.HORSE:
            moves.append([(0, 1), (-1, 1)])
            moves.append([(0, 1), (1, 1)])
            moves.append([(1, 0), (1, 1)])
            moves.append([(1, 0), (1, -1)])
            moves.append([(0, -1), (-1, -1)])
            moves.append([(0, -1), (1, -1)])
            moves.append([(-1, 0), (-1, 1)])
            moves.append([(-1, 0), (-1, -1)])

        elif self.pieceType == PieceType.ELEPHANT:
            moves.append([(0, 1), (-1, 1), (-1, 1)])
            moves.append([(0, 1), (1, 1), (1, 1)])
            moves.append([(1, 0), (1, 1), (1, 1)])
            moves.append([(1, 0), (1, -1), (1, -1)])
            moves.append([(0, -1), (-1, -1), (-1, -1)])
            moves.append([(0, -1), (1, -1), (1, -1)])
            moves.append([(-1, 0), (-1, 1), (-1, 1)])
            moves.append([(-1, 0), (-1, -1), (-1, -1)])

        return moves
