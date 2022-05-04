import classes.constant as constant
from classes.grid import Grid
from classes.camp import Camp
from classes.piece import PieceType


class MoveSet:
    def __init__(self, moves: [(int, int)]):
        self.moves = moves

    def getDest(self, board, origin: Grid, player: Camp):
        if self.validate(board, origin, player):
            row, col = (origin.row, origin.col)
            for dr, dc in self.moves:
                row += dr
                col += dc
            return Grid(row, col)
        else:
            return None

    def validate(self, board, origin: Grid, player: Camp):
        def isOutOfBound(row: int, col: int):
            return (row < constant.MIN_ROW or row > constant.MAX_ROW or
                    col < constant.MIN_COL or col > constant.MAX_COL)
        originPiece = board.get(origin.row, origin.col)
        numHurdles = 1 if originPiece.pieceType == PieceType.CANNON else 0
        row, col = (origin.row, origin.col)
        for i in range(len(self.moves)):
            (dr, dc) = self.moves[i]
            row += dr
            col += dc
            if isOutOfBound(row, col):
                return False

            piece = board.get(row, col)
            # Cannon cannot ever pass cannon
            if (piece and piece.pieceType == PieceType.CANNON and
                    originPiece.pieceType == PieceType.CANNON):
                return False

            if i == len(self.moves)-1:
                # Invalidate if some hurdles are left
                if numHurdles > 0:
                    return False
                # Invalidate if landing on an ally piece
                return not piece or piece.camp != player

            if piece:
                # Decrement number of hurdles left when passing a piece
                numHurdles -= 1
                if numHurdles < 0:
                    return False
        return True
