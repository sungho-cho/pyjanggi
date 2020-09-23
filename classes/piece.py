from enum import Enum

class PieceType(Enum):
    GENERAL = 1
    GUARD = 2
    HORSE = 3
    ELEPHANT = 4
    CHARIOT = 5
    CANNON = 6
    SOLDIER = 7


from termcolor import colored
from camp import Camp
from move import MoveSet
class Piece:
    def __init__(self, pieceType: PieceType):
        self.pieceType = pieceType
        self.camp = None

    def __str__(self):
        pieceToStr = {
            PieceType.GENERAL: "王",
            PieceType.GUARD: "士",
            PieceType.HORSE: "馬",
            PieceType.ELEPHANT: "象",
            PieceType.CHARIOT: "車",
            PieceType.CANNON: "包",
            PieceType.SOLDIER: "卒",
        }
        printStr = ""
        printStr += pieceToStr[self.pieceType]
        if self.camp == Camp.CHO:
            printStr = colored(printStr, 'green')
        elif self.camp == Camp.HAN:
            printStr = colored(printStr, 'red')
        return printStr

    def getJumpyMoveSets(self):
        moveSets = []

        if self.pieceType == PieceType.HORSE:
            moveSets.append(MoveSet([(0, 1), (-1, 1)], False))
            moveSets.append(MoveSet([(0, 1), (1, 1)], False))
            moveSets.append(MoveSet([(1, 0), (1, 1)], False))
            moveSets.append(MoveSet([(1, 0), (1, -1)], False))
            moveSets.append(MoveSet([(0, -1), (-1, -1)], False))
            moveSets.append(MoveSet([(0, -1), (1, -1)], False))
            moveSets.append(MoveSet([(-1, 0), (-1, 1)], False))
            moveSets.append(MoveSet([(-1, 0), (-1, -1)], False))

        elif self.pieceType == PieceType.ELEPHANT:
            moveSets.append(MoveSet([(0, 1), (-1, 1), (-1, 1)], False))
            moveSets.append(MoveSet([(0, 1), (1, 1), (1, 1)], False))
            moveSets.append(MoveSet([(1, 0), (1, 1), (1, 1)], False))
            moveSets.append(MoveSet([(1, 0), (1, -1), (1, -1)], False))
            moveSets.append(MoveSet([(0, -1), (-1, -1), (-1, -1)], False))
            moveSets.append(MoveSet([(0, -1), (1, -1), (1, -1)], False))
            moveSets.append(MoveSet([(-1, 0), (-1, 1), (-1, 1)], False))
            moveSets.append(MoveSet([(-1, 0), (-1, -1), (-1, -1)], False))

        return moveSets
