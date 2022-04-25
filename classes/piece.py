from classes.camp import Camp
from termcolor import colored
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
    from classes.move import MoveSet

    def __init__(self, pieceType: PieceType):
        self.pieceType = pieceType
        self.camp = None

    def _pieceToStr(self):
        pieceDict = {
            # PieceType.GENERAL: "王",
            PieceType.GUARD: "士",
            PieceType.HORSE: "馬",
            PieceType.ELEPHANT: "象",
            PieceType.CHARIOT: "車",
            PieceType.CANNON: "包",
            # PieceType.SOLDIER: "卒",
        }

        if self.pieceType in pieceDict:
            return pieceDict[self.pieceType]
        else:
            if self.pieceType == PieceType.GENERAL:
                if self.camp == Camp.CHO:
                    return "楚"
                else:
                    return "漢"
            elif self.pieceType == PieceType.SOLDIER:
                if self.camp == Camp.CHO:
                    return "卒"
                else:
                    return "兵"

    def __str__(self):
        printStr = self._pieceToStr()
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
